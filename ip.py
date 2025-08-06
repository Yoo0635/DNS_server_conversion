from fastapi import FastAPI, Query, HTTPException
import dns.resolver
import time
import socket
import pandas as pd

app = FastAPI()

@app.get("/ip")
def get_ip(domain: str = Query(...)):
    try:
        ips = dns.resolver.resolve(domain, 'A')
        iplist = [ip.to_text() for ip in ips]
        if not iplist:
            raise HTTPException(status_code=404, detail="ip가 1개밖에 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DNS 조회 실패: {str(e)}") #모름 gpt

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

    df = pd.DataFrame(results)
    df.to_csv("ip_응답속도_결과.csv", mode='a', index=False, header=not pd.io.common.file_exists("ip_응답속도_결과.csv"), encoding='utf-8-sig')

    return {
        "도메인": domain,
        "전체 결과": results,
        "가장 빠른 IP": fast["ip"],
        "응답 속도(ms)": fast["응답속도"]
    }
