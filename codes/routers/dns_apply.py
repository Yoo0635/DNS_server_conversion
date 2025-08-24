from fastapi import APIRouter
from codes.dns_auto import set_dns
from codes.dns_servers import dns_servers
from codes.schemas.dns_model import dnsIpRequest

router = APIRouter()

@router.post("/apply")
def dns_apply(request: dnsIpRequest):
    server = str(request.ip)

    try:
        set_dns(dns_servers[server])
        status = f'{server}로 설정 완료'
    except Exception as e:
        status = f'{server}로 설정 실패'

    return {"message" : status}