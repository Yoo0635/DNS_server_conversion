from fastapi import FastAPI, HTTPException
from urllib.parse import urlparse
import time, dns.resolver

app = FastAPI() # API 객체 생성

dns_servers =  { # DNS 서버 IP 목록
    "Google" : "8.8.8.8",
    "KISA" : "203.248.252.2",
    "KT" : "168.126.63.1",
    "SKB" : "219.250.36.130",
    "LGU+" : "164.124.101.2",
    "Kakao" : "203.248.252.2",
}

@app.get("/dns/{full_path:path}") # domain 입력받기 > 예 : localhost.8000/dns/naver.com
def read_root(full_path: str):
    parsed = urlparse(full_path if full_path.startswith("http") else "https://" + full_path)
    domain = parsed.netloc
    if not domain:
        raise HTTPException(status_code=400, detail="유효한 도메인을 입력해주세요.")
    
    result_all = [] 
    result_response = [] 
    
    for name, ip in dns_servers.items():
        tester = dns.resolver.Resolver()
        tester.nameservers = [ip]
        start_time = time.time()
        answer = tester.resolve(domain, 'A')
        end_time = time.time()
        response = round((end_time - start_time) * 1000, 2)

        result_all.append({
            "DNS 서버": name,
            "응답 시간": f"{response} ms"
        })
        result_response.append(response)

    min_server_name = None
    min_response = min(result_response)
    for item in result_all:
        if float(item["응답 시간"].replace(" ms", "")) == min_response:
            min_server_name = item["DNS 서버"]
    
    result_final = {
        "도메인" : domain,
        "전체 결과" : result_all,
        "최소 응답 서버" : min_server_name,
        "응답 시간" : f"{min_response} ms"
    }

    return result_final