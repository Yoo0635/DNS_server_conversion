from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import dns.resolver

app = FastAPI() # API 객체 생성

dns_servers =  { # DNS 서버 IP 목록
    "Google" : "8.8.8.8",
    "Cloudflare" : "1.1.1.1",
    "KT" : "168.126.63.1",
    "SKB" : "219.250.36.130",
    "LGU+" : "164.124.101.2",
    "Kakao" : "203.248.252.2",
    "Quad9" : "9.9.9.9"
}

@app.get("/dns/{domain}") # domain 입력받기 > 예 : localhost.8000/dns/naver.com
def read_root(domain: str):
    for name, ip in dns_servers.items():
        tester = dns.resolver.Resolver()
        tester.nameservers = [ip]
        start_time = time.time()
        answer = tester.resolve(domain, 'A')
        end_time = time.time()
        response = round((end_time - start_time) * 1000, 2)
        
        return{
            "DNS 서버" : name,
            "서버 IP" : answer,
            "DNS" : f"{response} ms"
        }

                
