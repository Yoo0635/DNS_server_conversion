import requests

BASE_URL = "http://localhost:8000"  # 백엔드 FastAPI 서버 주소

def get_dns_measure(domain, count=5):
    try:
        response = requests.get(f"{BASE_URL}/measure", params={"domain": domain, "count": count})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error in get_dns_measure: {e}")
        return None

def get_ip_response(domain):
    try:
        response = requests.get(f"{BASE_URL}/ip", params={"domain": domain})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error in get_ip_response: {e}")
        return None

def set_dns_server(dns_ip):
    try:
        response = requests.post(f"{BASE_URL}/apply_dns", json={"dns_ip": dns_ip})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error in set_dns_server: {e}")
        return None

def reset_dns_server():
    try:
        response = requests.post(f"{BASE_URL}/reset_dns")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error in reset_dns_server: {e}")
        return None
