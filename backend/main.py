from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
import sys
import os

# 새로운 라우터들 import
from routers.dns_measure import router as dns_measure_router
from routers.dns_apply import router as dns_apply_router
from routers.dns_reset import router as dns_reset_router
from routers.ip_measure import router as ip_measure_router

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Network Performance Optimizer API",
    description="DNS 및 IP 응답 속도 측정을 위한 API (개선된 버전)",
    version="2.0.0"
)

# CORS 설정 (크로스 플랫폼 지원)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 새로운 라우터 등록
app.include_router(dns_measure_router, prefix="/api/v1", tags=["DNS 측정"])
app.include_router(dns_apply_router, prefix="/api/v1", tags=["DNS 설정"])
app.include_router(dns_reset_router, prefix="/api/v1", tags=["DNS 설정"])
app.include_router(ip_measure_router, prefix="/api/v1", tags=["IP 측정"])

logger.info("✅ 모든 라우터가 성공적으로 로드되었습니다.")

@app.get("/")
def root():
    return {
        "message": "Network Performance Optimizer API (개선된 버전)",
        "version": "2.0.0",
        "features": [
            "Pydantic 유효성 검사",
            "체계적인 에러 핸들링",
            "크로스 플랫폼 DNS 설정",
            "상세한 로깅 시스템",
            "구조화된 라우터 분리"
        ],
        "endpoints": {
            "dns_measure": "/api/v1/measure?domain=example.com&count=5",
            "dns_apply": "/api/v1/apply (POST)",
            "dns_reset": "/api/v1/reset (POST)",
            "ip_measure": "/api/v1/ip?domain=example.com"
        },
        "documentation": "/docs"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "Network Performance Optimizer",
        "version": "2.0.0",
        "features": "개선된 버전 - Pydantic, 에러 핸들링, 크로스 플랫폼 지원"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9001, reload=True)
