from fastapi import HTTPException, APIRouter
from codes.dns_auto import set_dns
from codes.dns_servers import dns_servers
from codes.schemas.dns_model import DNSRequest

router = APIRouter()

@router.post("/apply")
def dns_apply(request : DNSRequest):
    server = request.server.strip()
    if server not in dns_servers:
        raise HTTPException(status_code=400, detail="지원되지 않는 DNS 서버입니다.")

    try:
        set_dns(dns_servers[server])
        status = f'{server}로 설정 완료'
    except Exception as e:
        status = f'{server}로 설정 실패'

    return {"message" : status}