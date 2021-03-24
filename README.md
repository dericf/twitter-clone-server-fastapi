# FastAPI - Twitter Clone

This is a project that is meant to explore the capabilities of FastAPI by building a real-world application - in this case a simple twitter clone.

## Installation/Setup

Make sure you have docker installed on your local machine.

Generate an application secret key by running `openssl rand -hex 32`

create a `.env` file and add the following environment variables

```
export POSTGRES_USER=postgresuser
export POSTGRES_PASSWORD=supersecretpassword
export POSTGRES_HOST=db
export POSTGRES_PORT=5432
export POSTGRES_DB=twitterdb
export ENV=dev
export SECRET_KEY="ASuperSecretKey"
export FIRST_SUPERUSER_EMAIL="super@user.com"
export FIRST_SUPERUSER_PASSWORD="asupersecretpassword"
export EMAIL_TEST_USER=john@doe.com
export PGADMIN_DEFAULT_EMAIL="admin@email.com"
export PGADMIN_DEFAULT_PASSWORD="supersecret"
export PGADMIN_LISTEN_PORT=80
```

run `source .env` to apply the environment variables

## Running in Development

All you need to run is `docker-compose up --build`

### Running Database Migrations (Alembic)

#### Run all migrations to current/highest state

Run `alembic migrate head`

#### Downgrade to the initial state (blank DB)

Run `alembic downgrade base`

#### Create a new migration version

Run `alembic revision -m "version tag"`

## Access Auto-Generated API Documentation

navigate to `localhost:8000/docs` or `localhost:8000/redocs`

## Deploy to Production Server

### Database
TODO

### Traefik + FastAPI docker on AWS

## Developer Docs and Examples

## FastAPI Docs
[https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)

## Starlette Docs
[https://www.starlette.io/](https://www.starlette.io/)

## FastAPI + SQLALchemy Tutorial
[https://fastapi.tiangolo.com/tutorial/sql-databases/](https://fastapi.tiangolo.com/tutorial/sql-databases/)

## Alembic Docs

## Docker Docs

## Docker Compose Docs

## Traefik docker image Docs

## FastAPI docker image Docs

## Terraform Docs

## AWS RDS Docs

## AWS ECS Docs