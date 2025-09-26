from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
import logging

from services.dns_service import DNSService
from dns_servers import dns_servers
from schemas.dns_models import DNSNameRequest, ApplyResponse

# 로깅 설정 (기본 설정이 이미 있으면 건너뛰기)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/apply", response_model=ApplyResponse)
def apply_dns_server(request: DNSNameRequest):
    """DNS 서버 적용"""
    server_name = request.name
    server_ip = dns_servers.get(server_name)
    
    if not server_ip:
        logger.error(f"DNS 서버를 찾을 수 없음: {server_name}")
        raise HTTPException(
            status_code=400,
            detail=f"'{server_name}'는 지원하지 않는 DNS 서버입니다."
        )
    
    try:
        logger.info(f"DNS 서버 적용 시작: {server_name} ({server_ip})")
        DNSService.set_dns(server_ip)
        
        return ApplyResponse(
            message=f"DNS 서버가 성공적으로 적용되었습니다.",
            server_name=server_name,
            server_ip=server_ip
        )
        
    except ValidationError as e:
        logger.error(f"DNS IP 유효성 검사 실패: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"{server_ip}는 유효한 IP 형식이 아닙니다."
        )
    except Exception as e:
        logger.error(f"DNS 서버 적용 실패: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"DNS 서버 적용 중 오류가 발생했습니다: {str(e)}"
        )
