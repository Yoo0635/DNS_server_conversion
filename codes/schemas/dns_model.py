from pydantic import BaseModel
from pydantic.networks import IPv4Address

class dnsIpRequest(BaseModel): # DNS IP 형식 유효성 검사
    ip : IPv4Address