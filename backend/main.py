from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mydns import router as dns_router
import uvicorn
import sys
import os

# ip.py 모듈 import (파일명 충돌 방지)
sys.path.append(os.path.dirname(__file__))
try:
    import ip as ip_module
    ip_router = ip_module.router
except ImportError:
    print("⚠️  ip.py 모듈을 찾을 수 없습니다. IP 측정 기능이 비활성화됩니다.")
    ip_router = None

app = FastAPI(
    title="Network Performance Optimizer API",
    description="DNS 및 IP 응답 속도 측정을 위한 API",
    version="1.0.0"
)

# CORS 설정 (크로스 플랫폼 지원)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(dns_router, prefix="/api/v1", tags=["DNS"])
if ip_router:
    app.include_router(ip_router, prefix="/api/v1", tags=["IP"])

@app.get("/")
def root():
    return {
        "message": "Network Performance Optimizer API",
        "version": "1.0.0",
        "endpoints": {
            "dns_measure": "/api/v1/measure?domain=example.com&count=5",
            "ip_measure": "/api/v1/ip?domain=example.com"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Network Performance Optimizer"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)
