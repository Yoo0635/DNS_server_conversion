from fastapi import FastAPI
from codes.routers.dns_measure import router as dns_measure
from codes.routers.dns_apply import router as dns_apply
from codes.routers.dns_reset import router as dns_reset
from codes.routers.dns_check import router as dns_check

app = FastAPI()

app.include_router(dns_measure)
app.include_router(dns_apply)
app.include_router(dns_reset)
app.include_router(dns_check)
# 인식 수정필요