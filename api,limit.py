from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import socket
import re


app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "요청이 너무 많습니다. 잠시 후 다시 시도해주세요."}
    )

def validate_domain(domain: str) -> tuple[bool, str]:
    if not domain or not domain.strip():
        return False, " 도메인이 입력되지 않았습니다."
    if '<' in domain or '>' in domain or 'script' in domain.lower():
        return False, " 위험한 문자가 포함되어 있습니다."
    pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.fullmatch(pattern, domain.strip()):
        return False, " 도메인 형식이 올바르지 않습니다."
    try:
        socket.gethostbyname(domain)
    except socket.gaierror:
        return False, " DNS 응답이 없습니다."
    return True, " 도메인이 정상입니다."


@app.get("/dns")
@limiter.limit("10/second") 
def dns_lookup(domain: str, request: Request):
    ok, msg = validate_domain(domain)
    if not ok:
        return JSONResponse(status_code=400, content={"detail": msg})
    return {"result": msg}