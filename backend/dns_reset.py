from fastapi import APIRouter
from dns_set import reset_dns
from pydantic import BaseModel

router = APIRouter()

class resetResponse(BaseModel):
    message: str

@router.post("/reset", response_model=resetResponse)
def reset_dns_api():
    try:
        reset_dns()
        return resetResponse(message="DNS 리셋 완료")
    except Exception as e:
        return resetResponse(message=f"DNS 리셋 실패: {str(e)}")


