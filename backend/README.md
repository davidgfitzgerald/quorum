# Quorum API Server

A FastAPI server for the backend API of the Quorum app.

## Run with Docker

From the `BACKEND` directory.

```shell
# Start the services
docker compose up --build --force-recreate -d

# Stop the services
docker compose stop
```

## Run locally

```shell

```

### Connect
2. Connect with `xh http://0.0.0.0:8000/api/v1/stub/ x==y` or `websocat ws://0.0.0.0:8000/api/v1/ws/rpc`
