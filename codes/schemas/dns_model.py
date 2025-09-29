from pydantic import BaseModel, field_validator, Field, StringConstraints
from pydantic.networks import IPv4Address
from typing import List, Annotated
from codes.dns_servers import dns_servers

class dnsIpRequest(BaseModel): # DNS IP 형식 유효성 검사
    ip : IPv4Address

class dnsNameRequest(BaseModel): # DNS 서버 이름 유효성 검사
    name : str
    @field_validator('name')
    def name_servers(cls,value):
        clean = value.strip()
        if clean not in dns_servers and clean.capitalize() not in dns_servers:
            raise ValueError(f"'{value}'는 유효한 DNS 서버가 아닙니다.")
        return clean

class statusResponse(BaseModel):
    message : str

class applyResponse(statusResponse):
    server_name: str = Field(..., description="설정한 DNS 서버 이름")
    server_ip: str = Field(..., description="설정한 DNS 서버 IP")

class resetResponse(statusResponse):
    pass

class measureResult(BaseModel):
    time: str = Field(..., description="측정 시간")
    server: str = Field(..., description="DNS 서버")
    domain: str = Field(..., description="도메인")
    avg: float = Field(..., description="평균 응답 시간(ms)")

class measureResponse(BaseModel):
    domain: str = Field(..., description="도메인")
    count: int = Field(..., description="측정 횟수")
    records: List[measureResult] = Field(..., description="측정 결과 리스트")