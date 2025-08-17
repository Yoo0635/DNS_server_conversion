# backend/main.py

from fastapi import FastAPI
from .api.dns_api import router as dns_router

app = FastAPI()

# dns_api.py에 있는 라우터를 포함하여 API 엔드포인트를 활성화합니다.
app.include_router(dns_router)

@app.get("/")
def root():
    return {"메시지": "FastAPI 서버가 실행 중입니다."}