from fastapi import APIRouter, HTTPException
import logging

from services.dns_service import DNSService
from schemas.dns_models import ResetResponse

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/reset", response_model=ResetResponse)
def reset_dns_server():
    """DNS 서버 리셋 (기본값으로 복구)"""
    try:
        logger.info("DNS 서버 리셋 시작")
        DNSService.reset_dns()
        
        return ResetResponse(
            message="DNS 서버가 성공적으로 리셋되었습니다."
        )
        
    except Exception as e:
        logger.error(f"DNS 서버 리셋 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"DNS 서버 리셋 중 오류가 발생했습니다: {str(e)}"
        )
