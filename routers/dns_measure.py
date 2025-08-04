from fastapi import APIRouter, Query
from datetime import datetime
from codes.dns_servers import dns_servers
import dns.resolver, time
import pandas as pd

router = APIRouter()

@router.get("/measure")
def measure_dns(domain: str = Query(...), count: int = Query(5, gt=0)):
    records = []
    for name, ip in dns_servers.items():
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [ip]

        times = []
        for i in range(count):
            try:
                start = time.time()
                resolver.resolve(domain, 'A')
                end = time.time()
                elapsed = round((end - start) * 1000, 2)
                times.append(elapsed)
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

    df = pd.DataFrame(records)
    df.to_csv("dns_응답속도_결과.csv", mode='a', index=False, header=not pd.io.common.file_exists("dns_응답속도_결과.csv"), encoding='utf-8-sig')

    return {
        "도메인": domain,
        "측정 횟수": count,
        "결과": records,
    }  
