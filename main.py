from fastapi import FastAPI, Request
import logging

app = FastAPI()

logging.basicConfig(
    filename="audit.log", 
    level=logging.INFO,           
    format="%(asctime)s - %(message)s" 
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    ip = request.client.host
    path = request.url.path 
    method = request.method  

    response = await call_next(request) 

    logging.info(f"[AUDIT] {ip}에서 {method} 요청 → {path}")

    return response

@app.get("/")
async def hello():
    return {"message": "안녕하세요"}