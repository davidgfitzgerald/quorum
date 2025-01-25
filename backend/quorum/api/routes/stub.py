from typing import Any, Dict

from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(tags=["stub"], prefix="/stub")


class RequestInfo(BaseModel):
    method: str
    url: str
    client_host: str
    headers: Dict[str, str]
    query_params: Dict[str, Any]


@router.get("/", response_model=RequestInfo)
async def stub_endpoint(request: Request):
    """Handler for GET requests at /stub that returns request information
    """
    return {
        "method": request.method,
        "url": str(request.url),
        "client_host": request.client.host if request.client else None,
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
    }
