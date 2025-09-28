from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError
import dns.resolver
import time
import pandas as pd
import logging
from datetime import datetime
from typing import List

from dns_servers import dns_servers
from schemas.dns_models import DomainRequest, MeasureResponse, MeasureResult

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/measure", response_model=MeasureResponse)
def measure_dns_performance(
    domain: str = Query(..., description="측정할 도메인"),
    count: int = Query(5, ge=1, le=20, description="측정 횟수 (1-20)")
):
    """DNS 서버별 응답 시간 측정"""
    
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
    
    logger.info(f"DNS 성능 측정 시작: {validated_domain} (횟수: {count})")
    
    records = []
    server_times = {}
    
    try:
        for server_name, server_ip in dns_servers.items():
            logger.info(f"측정 중: {server_name} ({server_ip})")
            
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [server_ip]
            resolver.timeout = 5.0  # 5초 타임아웃
            resolver.lifetime = 10.0  # 10초 생명주기
            
            times = []
            successful_queries = 0
            
            for i in range(count):
                try:
                    start_time = time.time()
                    resolver.resolve(validated_domain, 'A')
                    end_time = time.time()
                    
                    response_time = (end_time - start_time) * 1000  # ms로 변환
                    times.append(response_time)
                    successful_queries += 1
                    
                    logger.debug(f"{server_name} - 시도 {i+1}: {response_time:.2f}ms")
                    
                except Exception as e:
                    logger.warning(f"{server_name} - 시도 {i+1} 실패: {e}")
                    times.append(5000.0)  # 실패 시 5초로 설정
            
            if successful_queries > 0:
                avg_time = sum(times) / len(times)
                min_time = min(times)
                max_time = max(times)
                
                record = MeasureResult(
                    time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    server=server_name,
                    domain=validated_domain,
                    avg=round(avg_time, 2),
                    min_time=round(min_time, 2),
                    max_time=round(max_time, 2)
                )
                records.append(record)
                server_times[server_name] = avg_time
                
                logger.info(f"{server_name} 완료: 평균 {avg_time:.2f}ms")
            else:
                logger.error(f"{server_name} 모든 쿼리 실패")
        
        if not records:
            raise HTTPException(
                status_code=500,
                detail="모든 DNS 서버 측정에 실패했습니다."
            )
        
        # 가장 빠른/느린 서버 찾기
        fastest_server = min(server_times.items(), key=lambda x: x[1])[0]
        slowest_server = max(server_times.items(), key=lambda x: x[1])[0]
        
        # CSV 파일로 결과 저장
        try:
            df = pd.DataFrame([record.model_dump() for record in records])
            csv_filename = f"dns_응답속도_결과.csv"
            df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
            logger.info(f"결과 저장 완료: {csv_filename}")
        except Exception as e:
            logger.warning(f"CSV 저장 실패: {e}")
        
        response = MeasureResponse(
            domain=validated_domain,
            count=count,
            records=records,
            fastest_server=fastest_server,
            slowest_server=slowest_server
        )
        
        logger.info(f"DNS 측정 완료: {validated_domain}")
        return response
        
    except Exception as e:
        logger.error(f"DNS 측정 중 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"DNS 측정 중 오류가 발생했습니다: {str(e)}"
        )
