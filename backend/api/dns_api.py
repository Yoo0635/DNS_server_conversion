# backend/api/dns_api.py

from fastapi import APIRouter, HTTPException, Query
import dns.resolver
import time
import socket
import pandas as pd
from datetime import datetime

# utils 폴더에 있는 dns_utils.py에서 DNS 서버 정보를 가져옵니다.
from ..utils.dns_utils import DNS_SERVERS

router = APIRouter()

@router.get("/measure")
def measure_dns(domain: str = Query(...), count: int = Query(5, gt=0)):
    """
    DNS 서버별 응답 시간을 측정합니다.
    """
    if not domain:
        raise HTTPException(status_code=400, detail="도메인을 입력하세요.")

    records = []
    for name, ip in DNS_SERVERS.items():
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]

        times = []
        for _ in range(count):
            try:
                start = time.time()
                resolver.resolve(domain, 'A')
                end = time.time()
                times.append(round((end - start) * 1000, 2))
            except:
                times.append(float('inf'))

        avg = round(sum(times) / len(times), 2)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        records.append({
            "측정 시간": now,
            "DNS 서버": name,
            "도메인": domain,
            "평균 응답 시간(ms)": avg
        })
    
    # 응답 결과를 CSV 파일에 저장 (데이터 로깅)
    csv_name = "dns_응답속도_결과.csv"
    header_needed = not pd.io.common.file_exists(csv_name)
    pd.DataFrame(records).to_csv(
        csv_name, mode='a', index=False, header=header_needed, encoding='utf-8-sig'
    )
    
    return {"도메인": domain, "측정 횟수": count, "결과": records}

@router.get("/ip")
def get_ip(domain: str = Query(...)):
    """
    도메인의 IP를 찾고 각 IP의 응답 속도를 측정합니다.
    """
    try:
        ips = dns.resolver.resolve(domain, 'A')
        iplist = [ip.to_text() for ip in ips]
        if not iplist:
            raise HTTPException(status_code=404, detail="도메인에 연결된 IP 주소가 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DNS 조회 실패: {str(e)}")

    results = []
    for ip in iplist:
        try:
            start = time.time()
            s = socket.create_connection((ip, 80), timeout=2)
            end = time.time()
            s.close()
            how = round((end - start) * 1000, 2)
            results.append({"ip": ip, "응답속도": how})
        except Exception:
            results.append({"ip": ip, "응답속도": float('inf')})

    fast = min(results, key=lambda x: x["응답속도"])

    # 응답 결과를 CSV 파일에 저장 (데이터 로깅)
    df = pd.DataFrame(results)
    df.to_csv("ip_응답속도_결과.csv", mode='a', index=False, header=not pd.io.common.file_exists("ip_응답속도_결과.csv"), encoding='utf-8-sig')

    return {
        "도메인": domain,
        "전체 결과": results,
        "가장 빠른 IP": fast["ip"],
        "응답 속도(ms)": fast["응답속도"]
    }