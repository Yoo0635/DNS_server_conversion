from pydantic import BaseModel, field_validator, Field, StringConstraints
from pydantic.networks import IPv4Address
from typing import List, Annotated
from datetime import datetime
import re

class DNSIpRequest(BaseModel):
    """DNS IP 형식 유효성 검사"""
    ip: IPv4Address

class DNSNameRequest(BaseModel):
    """DNS 서버 이름 유효성 검사"""
    name: str
    
    @field_validator('name')
    def validate_name(cls, value):
        from dns_servers import dns_servers
        clean = value.strip()
        if clean not in dns_servers and clean.capitalize() not in dns_servers:
            raise ValueError(f"'{value}'는 유효한 DNS 서버가 아닙니다.")
        return clean

class DomainRequest(BaseModel):
    """도메인 유효성 검사"""
    domain: Annotated[
        str, 
        StringConstraints(
            strip_whitespace=True,
            min_length=3,
            max_length=253
        )
    ]
    
    @field_validator('domain')
    def validate_domain(cls, value):
        # 도메인 형식 검증
        if not re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$', value):
            raise ValueError("유효하지 않은 도메인 형식입니다.")
        return value.lower()

class StatusResponse(BaseModel):
    """기본 상태 응답"""
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ApplyResponse(StatusResponse):
    """DNS 적용 응답"""
    server_name: str = Field(..., description="설정한 DNS 서버 이름")
    server_ip: str = Field(..., description="설정한 DNS 서버 IP")

class ResetResponse(StatusResponse):
    """DNS 리셋 응답"""
    pass

class MeasureResult(BaseModel):
    """측정 결과 단일 항목"""
    time: str = Field(..., description="측정 시간")
    server: str = Field(..., description="DNS 서버")
    domain: str = Field(..., description="도메인")
    avg: float = Field(..., description="평균 응답 시간(ms)")
    min_time: float = Field(..., description="최소 응답 시간(ms)")
    max_time: float = Field(..., description="최대 응답 시간(ms)")

class MeasureResponse(BaseModel):
    """DNS 측정 응답"""
    domain: str = Field(..., description="도메인")
    count: int = Field(..., description="측정 횟수")
    records: List[MeasureResult] = Field(..., description="측정 결과 리스트")
    fastest_server: str = Field(..., description="가장 빠른 서버")
    slowest_server: str = Field(..., description="가장 느린 서버")

class IPResult(BaseModel):
    """IP 측정 결과 단일 항목"""
    ip: str = Field(..., description="IP 주소")
    response_time: float = Field(..., description="응답 시간(ms)")
    location: str = Field(default="Unknown", description="위치 정보")

class IPMeasureResponse(BaseModel):
    """IP 측정 응답"""
    domain: str = Field(..., description="도메인")
    results: List[IPResult] = Field(..., description="IP 측정 결과 리스트")
    fastest_ip: str = Field(..., description="가장 빠른 IP")
    slowest_ip: str = Field(..., description="가장 느린 IP")
