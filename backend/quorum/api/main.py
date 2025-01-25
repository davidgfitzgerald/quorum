from fastapi import APIRouter

from quorum.api.routes import stub
from quorum.api.routes import utils
from quorum.api.routes import ws

api_router = APIRouter()
api_router.include_router(stub.router)
api_router.include_router(utils.router)
api_router.include_router(ws.router)


# if settings.ENVIRONMENT == "local":
# api_router.include_router(private.router)
