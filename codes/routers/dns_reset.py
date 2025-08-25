from fastapi import APIRouter
from codes.services.dns_set import reset_dns

router = APIRouter()

@router.post("/reset")
def reset_dns_api():
    try:
        reset_dns()
        return {
            "message" : "DNS 리셋 완료"
        }
    except Exception as e:
        return{
            "message" : "DNS 리셋 실패"
        } 
    