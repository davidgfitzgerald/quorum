# Quorm

# Requirements

- [Docker](https://www.docker.com/) `>=20.10.23`

# Running With Docker

```shell
just start
```

# Running Frontend Locally

A svelte app server for the frontend of the Quorum app.

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

# Running Backend Locally

A FastAPI server for the backend API of the Quorum app.

## Local Requirements

- [python](https://www.python.org/downloads/) `>=3.13`
- [poetry](https://python-poetry.org/) `>=1.8.1`
- [uv](https://docs.astral.sh/uv) `>=0.5.26`
- [just](https://github.com/casey/just)

## Running Locally

1. Work from `backend/`
```shell
cd backend
```

2. Set up `.env`

```shell
cp .env.example .env
```

2. Install requirements
```shell
# Create virtual environment with uv
uv python install 3.13
uv venv --python 3.13
source .venv/bin/activate

# Install python packages with uv
uv sync
```

3. Run the server
```shell
# Run the backend server with fastapi
fastapi run --workers 1 quorum/main.py
```

## Connect

2. Connect with `xh http://0.0.0.0:8000/api/v1/stub/ x==y` or `websocat ws://0.0.0.0:8000/api/v1/ws/rpc`