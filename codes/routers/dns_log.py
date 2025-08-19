from fastapi import APIRouter, Request
import logging, os

router = APIRouter()

log_file = os.path.join(os.path.dirname(__file__), "audit.log")

logger = logging.getLogger("dns_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

@router.get("/dns_check")
async def dns_check(domain: str, request: Request):
    ip = request.client.host
    method = request.method
    path = request.url.path

    logger.info(f"[DNS_CHECK] {ip}에서 {method} 요청 → {path}?domain={domain}")

    return {"domain": domain, "status": "정상"}