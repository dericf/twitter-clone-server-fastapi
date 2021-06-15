# FastAPI
from fastapi import APIRouter, HTTPException, status, Request, Depends, BackgroundTasks

# SQLAlchemy
from sqlalchemy.orm import Session

# Types
from typing import List, Optional

# Custom Modules
from .. import schemas, crud
from ..background_functions.email_notifications import send_registration_confirmation_email
from ..dependencies import get_db, get_current_user

# Core Modules
from ..core import security
from ..core.config import settings
from ..core.utilities import generate_random_uuid

# Standard Library
import os

router = APIRouter(prefix="/users", tags=['users'])


@router.get("", response_model=List[schemas.UserResponse])
def get_one_or_all_users(userId: Optional[int] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Return either all users, or a single user with id == userId. Always returns a list.
    """
    if userId:
        users = [crud.get_user_by_id(db, userId)]
    else:
        users = crud.get_users(db, skip=skip, limit=limit)

    # TODO perhaps there is a better way of returning this model.
    # It seems like its trying to immidate graphql
    return [
        schemas.UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            bio=user.bio,
            birthdate=user.birthdate
        ) for user in users]


@router.get("/search/{usernameFragment}", response_model=List[schemas.UserResponse])
def get_one_or_all_users(usernameFragment: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Search for a user based on username.
    """
    users = crud.search_user_by_username_fragment(
        db, usernameFragment, skip, limit)

    # TODO perhaps there is a better way of returning this model.
    # It seems like its trying to immidate graphql
    return [
        schemas.UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            bio=user.bio,
            birthdate=user.birthdate
        ) for user in users]


@router.get("/me", response_model=schemas.User)
def get_authenticated_user(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    """Get the currently logged in user if there is one (testing purposes only)
    """
    return current_user


@router.post("", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, bg_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Create a new user record in the database and send a registration confirmation email
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    #
    # Generate a random uuid to email to the user
    #
    confirmation_key = generate_random_uuid()
    #
    # Create the new user
    #
    newUser: schemas.User = crud.create_user(
        db=db, user=user, confirmation_key=confirmation_key)
    bg_tasks.add_task(
        send_registration_confirmation_email,
        username=newUser.username,
        email=user.email,
        confirmation_key=confirmation_key
    )
    return newUser


@router.put('', response_model=schemas.UserUpdateResponseBody)
def update_user(request_body: schemas.UserUpdateRequestBody,
                db: Session = Depends(get_db),
                current_user: schemas.UserWithPassword = Depends(get_current_user)):
    """Update an authenticated user's username and/or bio.
    """
    # Check that password is correct
    if not security.verify_password(request_body.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")

    # Check if they are trying to update the username
    if request_body.newUsername is not None:
        # see if that username is available
        db_user_with_username = crud.get_user_by_username(
            db, request_body.newUsername)
        if db_user_with_username is not None:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Username already exists")

    # Update user attributes
    user = crud.update_user(db, current_user.id, request_body)
    return user


@router.delete('/', response_model=schemas.EmptyResponse)
def delete_user(request_body: schemas.UserDeleteRequestBody,
                db: Session = Depends(get_db),
                current_user: schemas.UserWithPassword = Depends(get_current_user)):
    if not security.verify_password(request_body.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    delete_successful = crud.delete_user(db, current_user.id)

    return schemas.EmptyResponse()


@router.post('/confirm-account/', response_model=schemas.EmptyResponse)
async def confirm_account(request_body: schemas.UserAccountConfirmationRequestBody, db: Session = Depends(get_db)):
    user: schemas.User = crud.get_user_by_confirmation_key(
        db, request_body.confirmationKey)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad key.")

    # correct confirmation key was passed

    crud.verify_account(db, user.id)

    return schemas.EmptyResponse()
