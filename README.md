# FastAPI - Twitter Clone

This is a project that is meant to explore the capabilities of FastAPI by building a real-world application - in this case a simple twitter clone.

[]()

## Installation/Setup

Make sure you have docker installed on your local machine.

Generate an application secret key by running `openssl rand -hex 32`

create a `.env` file and add the following environment variables

```
export LOCAL_POSTGRES_URL="postgresql://admin:secret@localhost:5433/twitterdb"
export LOCAL_DOCKER_INTERNAL_POSTGRES_URL="postgresql://admin:secret@db:5432/twitterdb"
export PRODUCTION_POSTGRES_URL="postgresql://admin:secret@<cloud-host>:5432/twitterdb"
export ENV=development
export SECRET_KEY="ASuperSecretKey"
export FIRST_SUPERUSER_EMAIL="super@user.com"
export FIRST_SUPERUSER_PASSWORD="asupersecretpassword"
export EMAIL_TEST_USER=john@doe.com
export SEND_GRID_API_KEY=<Your Send Grid API Key>
export PRODUCTION_CLIENT_HOST_URL="localhost:3000"
export SEND_GRID_FROM_EMAIL="account-verification@your-domain.com"
export PRODUCTION_DOMAIN_HOST="your-api-host-domain.com"
```

run `source .env` to apply the environment variables

## Running in Development

All you need to run is `docker-compose -f docker-compose-dev.yml up --build` and it will build the docker image based on `Dockerfile-dev` and will automatically handle hot-reloading while developing.

### Running Database Migrations (Alembic)

#### Downgrade to the initial state (blank DB)

Run `alembic downgrade base`

#### Run all migrations to current/highest state

Run `alembic upgrade head`

#### Create a new migration version

Run `alembic revision -m "version tag"`

## Access Auto-Generated API Documentation

navigate to `localhost:8001/docs` or `localhost:8001/redocs`

## Deploy to Production Server

[Great blog post here](https://dev.to/tiangolo/deploying-fastapi-and-other-apps-with-https-powered-by-traefik-5dik)

Create a new Linode Server

Add CNAME record to point to that server

SSH into your server `ssh root@your-domain.com`

run `apt update` to update package listing

run `apt upgrade` to actually install all latest packages

[Docker Install Scripts](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script)

[Docker Compose Install](https://docs.docker.com/compose/install/)

TODO: `apt install haveged`

`rsync -a --exclude 'pgdata' --exclude '__pycache__' --exclude 'venv' ./* root@twitter-clone-fastapi.programmertutor.com:/root/code/twitter-clone-server-fastapi`

_Note this doesn't send the .env file - must create that manually on the server once._

create the `docker-compose.traefik.yml file`
create the `docker-compose.override.yml file`

### Set up credentials for traefik dashboard basic auth.

create 3 new .env variables (USERNAME, PASSWORD and HASHED_PASSWORD)

get the value of `HASHED_PASSWORD` with `echo $(openssl passwd -apr1 $PASSWORD)`

### Set up traefik network for the first time

Create the traefik public network with `docker network create traefik-public`

### Run the main traefik container in the background

Run traefik docker container with `docker-compose -f docker-compose.traefik.yml up -d`

### Finally run the fastapi server docker container

Run the fastapi server with `docker-compose -f docker-compose-prod.yml up --build -d`

### Database

Create a new Postgres Database on AWS RDS and update the `PRODUCTION_POSTGRES_URL` in your `.env` file

---

## Developer Docs and Examples

### Python Types & Pydantic Models

[https://fastapi.tiangolo.com/python-types/](https://fastapi.tiangolo.com/python-types/)

[https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)

### FastAPI Docs

[https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

### Starlette Docs

[https://www.starlette.io/](https://www.starlette.io/)

### FastAPI + SQLALchemy Tutorial

[https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### Alembic Docs

### Docker Docs

### Docker Compose Docs

### Manual FastAPI Deployment Docs

https://fastapi.tiangolo.com/deployment/manually/

### Traefik docker image Docs

### FastAPI docker image Docs

https://fastapi.tiangolo.com/deployment/docker/

### Terraform Docs

### AWS RDS Docs

### AWS ECS Docs

### OpenAPI Spec Docs

https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.1.0.md#format

### Containerized VS Code Instances for development

https://code.visualstudio.com/docs/remote/containers

## References

[FastAPI — How to add basic and cookie authentication (by Nils de Bruin)](https://medium.com/data-rebels/fastapi-how-to-add-basic-and-cookie-authentication-a45c85ef47d3)
