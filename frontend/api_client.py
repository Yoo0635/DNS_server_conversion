# frontend/api_client.py

import requests
import json
import logging
from typing import Dict, List, Optional
import platform
import os

# 로깅 설정 (기본 설정이 이미 있으면 건너뛰기)
logger = logging.getLogger(__name__)

class NetworkAPIClient:
    """네트워크 성능 측정 API 클라이언트"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:9002"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        
        # 크로스 플랫폼 호환성을 위한 헤더 설정
        self.session.headers.update({
            'User-Agent': f'NetworkOptimizer/{platform.system()}/{platform.release()}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # 타임아웃 설정
        self.timeout = 30
        
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """API 요청을 수행하는 내부 메서드"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.ConnectionError:
            logger.error(f"서버 연결 실패: {self.base_url}")
            return {"error": "서버에 연결할 수 없습니다. 백엔드 서버가 실행 중인지 확인하세요."}
            
        except requests.exceptions.Timeout:
            logger.error(f"요청 타임아웃: {url}")
            return {"error": "요청 시간이 초과되었습니다."}
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP 오류: {e}")
            if e.response.status_code == 403:
                return {"error": f"관리자 권한이 필요합니다: {e.response.text}"}
            else:
                return {"error": f"서버 오류: {e.response.status_code}"}
            
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            return {"error": f"예상치 못한 오류가 발생했습니다: {str(e)}"}
    
    def health_check(self) -> Dict:
        """서버 상태 확인"""
        return self._make_request("GET", "/health")
    
    def measure_dns_performance(self, domain: str, count: int = 5) -> Dict:
        """DNS 서버별 응답 시간 측정"""
        if not domain:
            return {"error": "도메인을 입력하세요."}
            
        if count < 1 or count > 20:
            return {"error": "측정 횟수는 1-20 사이여야 합니다."}
            
        logger.info(f"DNS 성능 측정 시작: {domain} (횟수: {count})")
        
        params = {
            "domain": domain,
            "count": count
        }
        
        return self._make_request("GET", "/api/v1/measure", params=params)
    
    def measure_ip_performance(self, domain: str) -> Dict:
        """IP 주소별 응답 시간 측정"""
        if not domain:
            return {"error": "도메인을 입력하세요."}
            
        logger.info(f"IP 성능 측정 시작: {domain}")
        
        params = {"domain": domain}
        
        return self._make_request("GET", "/api/v1/ip", params=params)
    
    def get_server_info(self) -> Dict:
        """서버 정보 조회"""
        return self._make_request("GET", "/")
    
    def apply_dns_server(self, server_name: str) -> Dict:
        """DNS 서버 설정"""
        if not server_name:
            return {"error": "DNS 서버 이름을 입력하세요."}
            
        logger.info(f"DNS 서버 설정: {server_name}")
        
        data = {"name": server_name}
        
        return self._make_request("POST", "/api/v1/apply", json=data)
    
    def reset_dns_server(self) -> Dict:
        """DNS 서버 리셋"""
        logger.info("DNS 서버 리셋")
        
        return self._make_request("POST", "/api/v1/reset")

# 전역 API 클라이언트 인스턴스
api_client = NetworkAPIClient()

# 편의 함수들
def get_dns_measurements(domain: str, count: int = 5) -> Dict:
    """DNS 측정 결과를 가져오는 편의 함수"""
    return api_client.measure_dns_performance(domain, count)

def get_fastest_ip(domain: str) -> Dict:
    """가장 빠른 IP를 찾는 편의 함수"""
    return api_client.measure_ip_performance(domain)

def check_server_health() -> Dict:
    """서버 상태를 확인하는 편의 함수"""
    return api_client.health_check()

def apply_dns_server(server_name: str) -> Dict:
    """DNS 서버를 설정하는 편의 함수"""
    return api_client.apply_dns_server(server_name)

def reset_dns_server() -> Dict:
    """DNS 서버를 리셋하는 편의 함수"""
    return api_client.reset_dns_server()
