from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/dns_limit")
@limiter.limit("10/second")
async def dns_limit_endpoint(request: Request):
    return {"message": "DNS limit 적용 완료"}

#리밋코드