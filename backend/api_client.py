# backend/api_client.py

from flask import Flask, jsonify, request
import time
import socket
import dns.resolver

app = Flask(__name__)

# 공용 DNS 서버 리스트
PUBLIC_DNS_SERVERS = [
    "8.8.8.8",   # Google
    "8.8.4.4",   # Google
    "1.1.1.1",   # Cloudflare
    "1.0.0.1",   # Cloudflare
]

@app.route('/api/dns_measurements', methods=['GET'])
def get_dns_measurements():
    domain = request.args.get('domain', 'google.com')
    results = []

    for server in PUBLIC_DNS_SERVERS:
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [server]
        resolver.timeout = 5
        resolver.lifetime = 5

        start_time = time.time()
        try:
            answers = resolver.resolve(domain, 'A')
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            
            results.append({
                "DNS 서버": server,
                "평균 응답 시간(ms)": round(response_time_ms, 2)
            })
        except Exception as e:
            results.append({
                "DNS 서버": server,
                "평균 응답 시간(ms)": None
            })
            print(f"Error resolving with {server}: {e}")

    return jsonify({"결과": results})

@app.route('/api/fastest_ip', methods=['GET'])
def get_fastest_ip():
    domain = request.args.get('domain', 'google.com')
    results = []

    try:
        ip_addresses = [str(ip) for ip in dns.resolver.resolve(domain, 'A')]
    except Exception:
        ip_addresses = []

    for ip in ip_addresses:
        start_time = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        try:
            s.connect((ip, 80))
            end_time = time.time()
            response_time_ms = (end_time - start_time) * 1000
            results.append({
                "ip": ip,
                "응답속도": round(response_time_ms, 2)
            })
        except socket.error:
            pass
        finally:
            s.close()
            
    return jsonify({"전체 결과": results})

if __name__ == '__main__':
    app.run(port=5000, debug=True)