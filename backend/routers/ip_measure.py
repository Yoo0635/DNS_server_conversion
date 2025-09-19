from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError
import socket
import time
import pandas as pd
import logging
from datetime import datetime
from typing import List

from schemas.dns_models import DomainRequest, IPMeasureResponse, IPResult

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/ip", response_model=IPMeasureResponse)
def measure_ip_performance(
    domain: str = Query(..., description="측정할 도메인")
):
    """IP 주소별 응답 시간 측정"""
    
    # 도메인 유효성 검사
    try:
        domain_request = DomainRequest(domain=domain)
        validated_domain = domain_request.domain
    except ValidationError as e:
        logger.error(f"도메인 유효성 검사 실패: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"유효하지 않은 도메인 형식: {domain}"
        )
    
    logger.info(f"IP 성능 측정 시작: {validated_domain}")
    
    try:
        # 도메인의 모든 IP 주소 조회
        ip_addresses = []
        try:
            ip_list = socket.gethostbyname_ex(validated_domain)[2]
            ip_addresses = [ip for ip in ip_list if not ip.startswith('127.')]
        except socket.gaierror as e:
            logger.error(f"IP 주소 조회 실패: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"도메인 '{validated_domain}'의 IP 주소를 찾을 수 없습니다."
            )
        
        if not ip_addresses:
            raise HTTPException(
                status_code=400,
                detail=f"도메인 '{validated_domain}'에 유효한 IP 주소가 없습니다."
            )
        
        logger.info(f"발견된 IP 주소: {ip_addresses}")
        
        results = []
        ip_times = {}
        
        for ip in ip_addresses:
            logger.info(f"측정 중: {ip}")
            
            times = []
            successful_pings = 0
            
            # 각 IP에 대해 3번 측정
            for i in range(3):
                try:
                    start_time = time.time()
                    
                    # TCP 연결로 응답 시간 측정 (포트 80)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5.0)  # 5초 타임아웃
                    
                    result = sock.connect_ex((ip, 80))
                    end_time = time.time()
                    
                    sock.close()
                    
                    if result == 0:  # 연결 성공
                        response_time = (end_time - start_time) * 1000  # ms로 변환
                        times.append(response_time)
                        successful_pings += 1
                        logger.debug(f"{ip} - 시도 {i+1}: {response_time:.2f}ms")
                    else:
                        logger.warning(f"{ip} - 시도 {i+1} 연결 실패")
                        times.append(5000.0)  # 실패 시 5초로 설정
                        
                except Exception as e:
                    logger.warning(f"{ip} - 시도 {i+1} 오류: {e}")
                    times.append(5000.0)
            
            if successful_pings > 0:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                
                # 간단한 위치 정보 (실제로는 GeoIP 서비스 사용 가능)
                location = "Unknown"
                if ip.startswith("8.8."):
                    location = "Google"
                elif ip.startswith("1.1.1.1"):
                    location = "Cloudflare"
                
                result = IPResult(
                    ip=ip,
                    response_time=round(avg_time, 2),
                    location=location
                )
                results.append(result)
                ip_times[ip] = avg_time
                
                logger.info(f"{ip} 완료: 평균 {avg_time:.2f}ms")
            else:
                logger.error(f"{ip} 모든 연결 실패")
        
        if not results:
            raise HTTPException(
                status_code=500,
                detail="모든 IP 주소 측정에 실패했습니다."
            )
        
        # 가장 빠른/느린 IP 찾기
        fastest_ip = min(ip_times.items(), key=lambda x: x[1])[0]
        slowest_ip = max(ip_times.items(), key=lambda x: x[1])[0]
        
        # CSV 파일로 결과 저장
        try:
            df = pd.DataFrame([result.model_dump() for result in results])
            csv_filename = f"ip_응답속도_결과.csv"
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            logger.info(f"결과 저장 완료: {csv_filename}")
        except Exception as e:
            logger.warning(f"CSV 저장 실패: {e}")
        
        response = IPMeasureResponse(
            domain=validated_domain,
            results=results,
            fastest_ip=fastest_ip,
            slowest_ip=slowest_ip
        )
        
        logger.info(f"IP 측정 완료: {validated_domain}")
        return response
        
    except Exception as e:
        logger.error(f"IP 측정 중 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"IP 측정 중 오류가 발생했습니다: {str(e)}"
        )
