# Quorm

# Frontend

## Local Requirements

- Node `>=23.7.0`
- npm `>=11.1.0`

### Node/npm versioning

If you use [nvm](https://github.com/nvm-sh/nvm) you can install the latest `node` and `npm` with:

```shell
nvm install node
npm install -g npm@latest
```

then verify versions:

```shell
node --version
npm --version
```

## Running Locally

```shell
cd frontend
npm install
npm run open
```

# Backend

A FastAPI server for the backend API of the Quorum app.

## Run with Docker

1. Set up `.env`

```shell
cp .env.example .env
```

2. Run docker container(s)

```shell
# Work from backend dir
cd backend

# Start the services
docker compose up --build --force-recreate -d

# Stop the services
docker compose stop
```

## Local Requirements

- [poetry](https://python-poetry.org/) `>=1.8.1`
- [uv](https://docs.astral.sh/uv) `>=0.5.26`
- [just](https://github.com/casey/just)

## Running Locally

```shell
# Work from backend dir
cd backend

# Create virtual environment with uv
uv python install 3.13
uv venv --python 3.13
source .venv/bin/activate

# Install python packages with uv
uv sync

# Run the backend server with fastapi
fastapi run --workers 1 quorum/main.py
```

## Connect

2. Connect with `xh http://0.0.0.0:8000/api/v1/stub/ x==y` or `websocat ws://0.0.0.0:8000/api/v1/ws/rpc`