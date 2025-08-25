from pydantic import BaseModel, field_validator
from pydantic.networks import IPv4Address
from codes.dns_servers import dns_servers

class dnsIpRequest(BaseModel): # DNS IP 형식 유효성 검사
    ip : IPv4Address

class dnsNameRequest(BaseModel): # DNS 서버 이름 유효성 검사
    name : str
    @field_validator('name')
    def name_servers(cls,value):
        if value not in dns_servers:
            raise ValueError(f"'{value}'는 유효한 DNS 서버가 아닙니다.")
        return value;

class statusResponse(BaseModel):
    message : str