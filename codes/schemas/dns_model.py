from pydantic import BaseModel

class DNSRequest(BaseModel):
    server : str