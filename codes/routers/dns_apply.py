from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from codes.services.dns_set import set_dns
from codes.dns_servers import dns_servers
from codes.schemas.dns_model import dnsIpRequest, dnsNameRequest, statusResponse

router = APIRouter()

@router.post("/apply", response_model=statusResponse)
def dns_apply(request: dnsNameRequest): 
    server_name = request.name
    server_ip = dns_servers.get(server_name)
    
    try:
        dnsIpRequest(ip=server_ip)
    except ValidationError:
        raise HTTPException(
            status_code=500,
            detail=f"{server_ip}는 유효한 IP 형식이 아닙니다."
        )
    
    try:
        set_dns(server_ip)
        status = f'{server_name}로 설정 완료'
    except Exception as e:
        status = f'{server_name}로 설정 실패'

    return {"message" : status}