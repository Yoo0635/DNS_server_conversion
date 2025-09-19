import platform, subprocess

def detect_adapter_win(): # Win 어댑터 탐지
    result = subprocess.run(
        'netsh interface show interface',
        shell = True, capture_output= True, text= True, encoding='utf-8'
    )
    lines = result.stdout.splitlines()

    for line in lines:
        if "Connected" in line or "연결됨" in line:
            return line.strip().split()[-1]
    raise Exception("Windows 어댑터 이름을 찾을 수 없습니다.")
    
def detect_adapter_mac(): # mac 어댑터 탐지
    result = subprocess.run(
        'networksetup -listallnetworkservices',
        shell = True, capture_output= True, text= True, encoding='utf-8'
    )
    lines = result.stdout.splitlines()

    # 실제 네트워크 서비스만 찾기
    for line in lines:
        line = line.strip()
        # *로 시작하지 않고, 실제 네트워크 서비스인 경우
        if line and not line.startswith("*") and not line.startswith("An asterisk"):
            # Wi-Fi, Ethernet 등 실제 네트워크 서비스 확인
            if any(keyword in line.lower() for keyword in ['wi-fi', 'ethernet', 'usb', 'thunderbolt']):
                return line
    
    # 위 조건에 맞지 않으면 첫 번째 활성화된 서비스 반환
    for line in lines:
        line = line.strip()
        if line and not line.startswith("*") and not line.startswith("An asterisk"):
            return line
            
    raise Exception("Mac 어댑터 이름을 찾을 수 없습니다.")

def set_dns(dns_ip : str): # DNS 설정
    if not dns_ip:
        raise ValueError("DNS IP가 None입니다.")
    os_name = platform.system() 
    if(os_name == "Windows"):
        adapter = detect_adapter_win()
        command = f'netsh interface ip set dns name="{adapter}" static {dns_ip}'
    elif(os_name == "Darwin"):
        adapter = detect_adapter_mac()
        command = f'networksetup -setdnsservers "{adapter}" {dns_ip}'
    else:
        raise Exception("Windows, Mac만 지원합니다.")
    
    # 디버깅을 위한 로그 추가
    print(f"🔍 DNS 설정 디버깅:")
    print(f"   OS: {os_name}")
    print(f"   어댑터: {adapter}")
    print(f"   DNS IP: {dns_ip}")
    print(f"   실행할 명령어: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")
    
    # 결과 확인
    print(f"   반환 코드: {result.returncode}")
    print(f"   stdout: {result.stdout.strip()}")
    print(f"   stderr: {result.stderr.strip()}")
    
    if result.returncode != 0:
        if os_name == "Darwin":
            raise Exception(f"DNS 설정 실패: {result.stderr.strip()}")
        else:
            raise Exception(f"DNS 설정 실패: {result.stderr.strip()}")
    else:
        print(f"✅ DNS 설정 성공!")

def reset_dns(): # DNS 리셋
    os_name = platform.system()
    if(os_name == "Windows"):
        adapter = detect_adapter_win()
        command = f'netsh interface ip set dns name="{adapter}" dhcp'
    elif(os_name == "Darwin"):
        adapter = detect_adapter_mac()
        command = f'networksetup -setdnsservers "{adapter}" Empty'
    else:
        raise Exception("Windows, Mac만 지원합니다.")
    
    # 디버깅을 위한 로그 추가
    print(f"🔍 DNS 리셋 디버깅:")
    print(f"   OS: {os_name}")
    print(f"   어댑터: {adapter}")
    print(f"   실행할 명령어: {command}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")
    
    # 결과 확인
    print(f"   반환 코드: {result.returncode}")
    print(f"   stdout: {result.stdout.strip()}")
    print(f"   stderr: {result.stderr.strip()}")
    
    if result.returncode != 0:
        if os_name == "Darwin":
            raise Exception(f"DNS 리셋 실패: {result.stderr.strip()}")
        else:
            raise Exception(f"DNS 리셋 실패: {result.stderr.strip()}")
    else:
        print(f"✅ DNS 리셋 성공!")