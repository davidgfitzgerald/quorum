from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from quorum.core.config import settings
from quorum.api.main import api_router


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_headers=["*"],
        allow_methods=["*"],
        allow_origins=["*"],
        # TODO: Allow setting '*' with the BACKEND_CORS_ORIGINS env var
        # allow_origins=settings.all_cors_origins,
    )

app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

app.include_router(api_router, prefix=settings.API_V1_STR)
