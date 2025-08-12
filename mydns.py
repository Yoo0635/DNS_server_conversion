from fastapi import APIRouter, HTTPException, Query
import dns.resolver
import time
import pandas as pd
from datetime import datetime
from dns_servers import dns_servers

router = APIRouter()

@router.get("/measure")
def measure_dns(domain: str = Query(...), count: int = Query(5, gt=0)):
    if not domain:
        raise HTTPException(status_code=400, detail="도메인을 입력하세요.")

    records = []
    for name, ip in dns_servers.items():
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

    csv_name = "dns_응답속도_결과.csv"
    header_needed = not pd.io.common.file_exists(csv_name)
    pd.DataFrame(records).to_csv(
        csv_name, mode='a', index=False, header=header_needed, encoding='utf-8-sig'
    )

    return {"도메인": domain, "측정 횟수": count, "결과": records}
