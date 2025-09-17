from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import dns.resolver
import time
import pandas as pd
from datetime import datetime
from dns_servers import dns_servers

# 현재 사용 중인 DNS 서버를 관리하는 전역 변수
current_dns_server = "8.8.8.8"

router = APIRouter()

# DNS 변경 요청을 위한 모델
class DNSChangeRequest(BaseModel):
    new_dns: str

@router.get("/measure")
def measure_dns(domain: str = Query(...), count: int = Query(5, gt=0)):
    if not domain:
        raise HTTPException(status_code=400, detail="도메인을 입력하세요.")
    
    # 도메인 정리 (URL에서 도메인만 추출)
    domain = clean_domain(domain)
    
    if not is_valid_domain(domain):
        raise HTTPException(status_code=400, detail=f"유효하지 않은 도메인: {domain}")

    # 실제 측정 로직
    records = []
    # dns_servers 딕셔너리를 사용해 측정
    for name, ip in dns_servers.items():
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]

        times = []
        for _ in range(count):
            try:
                start = time.time()
                # 타임아웃 설정 (2초)
                resolver.timeout = 2
                resolver.lifetime = 2
                resolver.resolve(domain, 'A')
                end = time.time()
                times.append(round((end - start) * 1000, 2))
            except Exception:
                times.append(float('inf'))

        avg = round(sum(times) / len(times), 2)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records.append({
            "측정 시간": now,
            "DNS 서버 이름": name,
            "DNS 서버 IP": ip,
            "도메인": domain,
            "평균 응답 시간(ms)": avg
        })

    # CSV 저장
    csv_name = "dns_응답속도_결과.csv"
    header_needed = not pd.io.common.file_exists(csv_name)
    pd.DataFrame(records).to_csv(
        csv_name, mode='a', index=False, header=header_needed, encoding='utf-8-sig'
    )

    return {"도메인": domain, "측정 횟수": count, "결과": records}

<<<<<<< HEAD
@router.post("/change-dns")
def change_dns_server(request: DNSChangeRequest):
    global current_dns_server
    new_dns_ip = request.new_dns
    
    current_dns_server = new_dns_ip
    
    return {"status": "success", "message": f"DNS 서버가 {new_dns_ip}로 변경되었습니다."}

@router.post("/reset-dns")
def reset_dns_server():
    global current_dns_server
    # 기본 DNS 서버로 재설정
    current_dns_server = "8.8.8.8"
    return {"status": "success", "message": "DNS 서버가 기본값으로 초기화되었습니다."}

@router.get("/current-dns")
def get_current_dns():
    global current_dns_server
    return {"current_dns": current_dns_server}
=======
def clean_domain(domain):
    """도메인 정리"""
    # http:// 또는 https:// 제거
    if domain.startswith('http://'):
        domain = domain[7:]
    elif domain.startswith('https://'):
        domain = domain[8:]
    
    # www. 제거
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # 경로 제거
    if '/' in domain:
        domain = domain.split('/')[0]
    
    # 포트 번호 제거
    if ':' in domain:
        domain = domain.split(':')[0]
    
    return domain

def is_valid_domain(domain):
    """도메인 유효성 검사"""
    import re
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return re.match(pattern, domain) is not None
>>>>>>> 2e01351 (tkinter기반)
