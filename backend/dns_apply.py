from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from dns_set import set_dns
from dns_servers import dns_servers
from pydantic import BaseModel

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
    
    try:
        set_dns(server_ip)
        status = f'{server_name}로 설정 완료'
    except Exception as e:
        status = f'{server_name}로 설정 실패: {str(e)}'

    return applyResponse(message=status, server_name=server_name, server_ip=server_ip)


