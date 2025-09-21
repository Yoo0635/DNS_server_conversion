from fastapi import APIRouter, HTTPException
from services.dns_service import DNSService
from pydantic import BaseModel
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class resetResponse(BaseModel):
    message: str

@router.post("/reset", response_model=resetResponse)
def reset_dns_api():
    logger.info("DNS 리셋 시작")
    
    try:
        DNSService.reset_dns()
        logger.info("DNS 리셋 성공")
        return resetResponse(message="DNS 리셋 완료")
    except PermissionError as e:
        error_msg = str(e)
        logger.warning(f"DNS 리셋 실패 - 권한 부족: {error_msg}")
        raise HTTPException(
            status_code=403,
            detail=f"DNS 리셋을 위해 관리자 권한이 필요합니다. 터미널에서 sudo로 실행해주세요: {error_msg}"
        )
    except Exception as e:
        error_msg = str(e)
        logger.error(f"DNS 리셋 실패: {error_msg}")
        raise HTTPException(
            status_code=500,
            detail=f"DNS 리셋 중 오류가 발생했습니다: {error_msg}"
        )


