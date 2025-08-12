from fastapi import FastAPI
from dns import router as dns_router

app = FastAPI()
app.include_router(dns_router)

@app.get("/")
def root():
    return {"ok": True}
