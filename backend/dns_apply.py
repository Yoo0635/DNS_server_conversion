from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from services.dns_service import DNSService
from dns_servers import dns_servers
from pydantic import BaseModel
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

class dnsNameRequest(BaseModel):
    name: str

class applyResponse(BaseModel):
    message: str
    server_name: str
    server_ip: str

@router.post("/apply", response_model=applyResponse)
def dns_apply(request: dnsNameRequest): 
    server_name = request.name
    server_ip = dns_servers.get(server_name)
    
    if not server_ip:
        raise HTTPException(
            status_code=400,
            detail=f"'{server_name}'는 유효한 DNS 서버가 아닙니다."
        )
    
    logger.info(f"DNS 서버 적용 시작: {server_name} ({server_ip})")
    
    try:
        DNSService.set_dns(server_ip)
        status = f'{server_name}로 설정 완료'
        logger.info(f"DNS 서버 적용 성공: {server_name}")
    except Exception as e:
        error_msg = str(e)
        logger.error(f"DNS 서버 적용 실패: {error_msg}")
        
        # 모든 DNS 설정 오류를 403으로 처리 (관리자 권한 필요)
        raise HTTPException(
            status_code=403,
            detail=f"DNS 설정을 위해 관리자 권한이 필요합니다. 터미널에서 sudo로 실행해주세요."
        )

    return applyResponse(message=status, server_name=server_name, server_ip=server_ip)


