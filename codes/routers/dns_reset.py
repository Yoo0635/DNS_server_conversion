from fastapi import APIRouter
from codes.services.dns_set import reset_dns
from codes.schemas.dns_model import resetResponse

router = APIRouter()

@router.post("/reset", response_model=resetResponse)
def reset_dns_api():
    try:
        reset_dns()
        return resetResponse(message="DNS 리셋 완료")
    except Exception as e:
        return resetResponse(message="DNS 리셋 실패")
    