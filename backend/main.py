"""
Network Performance Optimizer - FastAPI Backend
DNS 및 IP 응답 속도 측정을 위한 API 서버
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# FastAPI 앱 생성
app = FastAPI(
    title="Network Performance Optimizer API",
    description="DNS 및 IP 응답 속도 측정을 위한 API",
    version="3.1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(dns_measure_router, prefix="/api/v1", tags=["DNS 측정"])
app.include_router(dns_apply_router, prefix="/api/v1", tags=["DNS 설정"])
app.include_router(dns_reset_router, prefix="/api/v1", tags=["DNS 설정"])
app.include_router(ip_measure_router, prefix="/api/v1", tags=["IP 측정"])

logger.info("✅ 모든 라우터가 성공적으로 로드되었습니다.")

@app.get("/")
def root():
    """API 루트 엔드포인트"""
    return {
        "message": "Network Performance Optimizer API",
        "version": "3.1.0",
        "features": [
            "DNS 성능 측정",
            "IP 응답 속도 측정", 
            "크로스 플랫폼 DNS 설정",
            "실시간 시각화"
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
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy", 
        "service": "Network Performance Optimizer",
        "version": "3.1.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=9002, reload=False)
