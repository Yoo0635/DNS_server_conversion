from fastapi import APIRouter, Query, HTTPException
import dns.resolver
import time
import socket
import pandas as pd
from datetime import datetime
import logging

router = APIRouter()

@router.get("/ip")
def get_ip(domain: str = Query(...)):
    # 도메인 정리
    domain = clean_domain(domain)
    
    if not is_valid_domain(domain):
        raise HTTPException(status_code=400, detail=f"유효하지 않은 도메인: {domain}")
    
    try:
        ips = dns.resolver.resolve(domain, 'A')
        iplist = [ip.to_text() for ip in ips]
        if not iplist:
            raise HTTPException(status_code=404, detail="ip가 1개밖에 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DNS 조회 실패: {str(e)}")

    # ------- 응답 생성 로직 -------
    results = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for ip in iplist:
        try:
            start = time.time()
            s = socket.create_connection((ip, 80), timeout=2)
            end = time.time()
            s.close()
            response_time = round((end - start) * 1000, 2)
            results.append({
                "측정 시간": now,
                "IP 주소": ip,
                "도메인": domain,
                "응답속도(ms)": response_time
            })
        except Exception:
            results.append({
                "측정 시간": now,
                "IP 주소": ip,
                "도메인": domain,
                "응답속도(ms)": float('inf')
            })

    # 유효한 결과만 필터링하여 가장 빠른 IP 찾기
    valid_results = [r for r in results if r["응답속도(ms)"] != float('inf')]
    if valid_results:
        fastest = min(valid_results, key=lambda x: x["응답속도(ms)"])
    else:
        fastest = {"IP 주소": "N/A", "응답속도(ms)": float('inf')}

    # CSV 파일에 저장
    csv_name = "ip_응답속도_결과.csv"
    header_needed = not pd.io.common.file_exists(csv_name)
    pd.DataFrame(results).to_csv(
        csv_name, mode='a', index=False, header=header_needed, encoding='utf-8-sig'
    )

    return {
        "도메인": domain,
        "측정 시간": now,
        "전체 결과": results,
        "가장 빠른 IP": fastest["IP 주소"],
        "응답 속도(ms)": fastest["응답속도(ms)"],
        "측정된 IP 수": len(iplist),
        "성공한 IP 수": len(valid_results)
    }

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
