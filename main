from fastapi import FastAPI, HTTPException, Query
import dns.resolver
import time
import pandas as pd
from datetime import datetime

app = FastAPI()

dns_servers = {
    "Google": "8.8.8.8",
    "KT": "168.126.63.1",
    "SKB": "219.250.36.130",
    "LGU+": "164.124.101.2",
    "KISA": "203.248.252.2"
}

@app.get("/measure")
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
        "결과": records
    }
