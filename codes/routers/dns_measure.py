from fastapi import APIRouter, Query
from datetime import datetime
from codes.dns_servers import dns_servers
from codes.schemas.dns_model import measureResponse, measureResult
import dns.resolver, time
import pandas as pd

router = APIRouter()

@router.get("/measure", response_model=measureResponse)
def measure_dns(domain: str = Query(..., description="측정 도메인"), count: int = Query(5, gt=0)):
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
        records.append(
            measureResult(
                time=now, server=name, domain=domain, avg=avg
            )
        )   

    df = pd.DataFrame(records) # pandas 
    df.to_csv("dns_응답속도_결과.csv", mode='a', index=False, header=not pd.io.common.file_exists("dns_응답속도_결과.csv"), encoding='utf-8-sig')

    return measureResponse(domain = domain, count=count, records=records)
