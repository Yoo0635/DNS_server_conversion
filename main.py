from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from codes.routers.dns_measure import router as dns_measure
from codes.routers.dns_apply import router as dns_apply
from codes.routers.dns_reset import router as dns_reset
from codes.routers.dns_check import router as dns_check
from codes.routers.dns_limit import router as dns_limit

app = FastAPI()

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요."}
    )

app.include_router(dns_measure)
app.include_router(dns_apply)
app.include_router(dns_reset)
app.include_router(dns_check)
app.include_router(dns_limit)