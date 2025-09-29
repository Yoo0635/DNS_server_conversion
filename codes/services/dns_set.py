import platform, subprocess

def detect_adapter(): # Win 어댑터 탐지
    result = subprocess.run(
        'netsh interface show interface',
        shell = True, capture_output= True, text= True, encoding='utf-8'
    )
    lines = result.stdout.splitlines()

    for line in lines:
        if "Connected" in line or "연결됨" in line:
            return line.strip().split()[-1]
    raise Exception("Windows 어댑터 이름을 찾을 수 없습니다.")
    

def set_dns(dns_ip : str): # DNS 설정
    if not dns_ip:
        raise ValueError("DNS IP가 None입니다.")
    os_name = platform.system() 
    if(os_name == "Windows"):
        adapter = detect_adapter()
        command = f'netsh interface ip set dns name="{adapter}" static {dns_ip}'
    else:
        raise Exception("Windows만 지원합니다.")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")

    if(result.returncode != 0):
        raise Exception(f"DNS 설정 실패 {result.stderr.strip()}")

def reset_dns(): # DNS 리셋
    os_name = platform.system()
    if(os_name == "Windows"):
        adapter = detect_adapter()
        command = f'netsh interface ip set dns name="{adapter}" dhcp'
    
    else:
        raise Exception("Windows만 지원합니다.")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")