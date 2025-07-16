def is_not_empty(domain: str) -> bool:
    return bool(domain and domain.strip())

def contains_malicious_code(domain: str) -> bool:
    lower = domain.lower()
    return any(tag in lower for tag in ['<script', '</script', '<', '>', '"', "'"])

def is_valid_format(domain: str) -> bool:
    pattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.fullmatch(pattern, domain.strip()))

def can_resolve_dns(domain: str) -> bool:
    try:
        socket.gethostbyname(domain)
        return True
    except socket.gaierror:
        return False

def validate_domain(domain: str) -> tuple[bool, str]:
    if not is_not_empty(domain):
        return False, "도메인이 입력되지 않았습니다. (400 Bad Request)"
    
    if contains_malicious_code(domain):
        return False, "도메인에 스크립트 또는 위험한 문자가 포함되어 있습니다. (422 Unprocessable Entity)"
    
    if not is_valid_format(domain):
        return False, "도메인 형식이 잘못되었습니다. 예: example.com (422 Unprocessable Entity)"
    
    if not can_resolve_dns(domain):
        return False, "DNS 서버에서 해당 도메인에 응답하지 않습니다. (408 Timeout)"
    
    return True, "도메인이 정상적으로 통과되었습니다." 
    #커밋이 이상해


