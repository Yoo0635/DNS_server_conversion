import platform
import subprocess
import logging
from typing import Optional
from schemas.dns_models import DNSIpRequest
# AdminChecker 제거됨 - UAC로 대체
import ctypes
import sys
import re

# 로깅 설정 (기본 설정이 이미 있으면 건너뛰기)
logger = logging.getLogger(__name__)

class DNSService:
    """DNS 설정 및 관리 서비스"""
    
    @staticmethod
    def detect_adapter_win() -> str:
        """Windows 네트워크 어댑터 탐지 (Loopback 제외, 연결된 실제 어댑터 우선)"""
        try:
            # 인터페이스 상태를 더 풍부하게 제공
            result = subprocess.run(
                'netsh interface show interface',
                shell=True,
                capture_output=True
            )
            def _dec(b):
                return (b.decode('cp949', errors='ignore') if isinstance(b, (bytes, bytearray)) else b) or ''
            stdout = _dec(result.stdout)
            stderr = _dec(result.stderr)
            
            if result.returncode != 0:
                raise Exception(f"Windows 어댑터 탐지 실패: {stderr}")
            
            lines = stdout.splitlines() if stdout else []
            candidates = []
            for line in lines:
                if not line.strip() or line.lower().startswith('admin'):
                    continue
                # 컬럼: Admin State  State   Type    Interface Name
                parts = line.split()
                if len(parts) < 4:
                    continue
                # 이름은 4번째 이후 전체
                name = ' '.join(parts[3:]).strip()
                state = ' '.join(parts[1:3]).lower()
                if (('connected' in state) or ('연결됨' in state)) and ('loopback' not in name.lower()) and ('pseudo' not in name.lower()):
                    candidates.append(name)
            # 우선순위: Ethernet/이더넷 > Wi-Fi/무선 > 그 외
            def score(n: str) -> int:
                nl = n.lower()
                if 'ethernet' in nl or '이더넷' in nl:
                    return 3
                if 'wi-fi' in nl or 'wifi' in nl or '무선' in nl or 'wlan' in nl:
                    return 2
                return 1
            if candidates:
                adapter_name = sorted(candidates, key=lambda x: -score(x))[0]
                logger.info(f"Windows 어댑터 감지: {adapter_name}")
                return adapter_name
            
            raise Exception("Windows 어댑터 이름을 찾을 수 없습니다.")
            
        except Exception as e:
            logger.error(f"Windows 어댑터 탐지 오류: {e}")
            raise
    
    @staticmethod
    def detect_adapter_mac() -> str:
        """macOS 네트워크 어댑터 탐지"""
        try:
            result = subprocess.run(
                'networksetup -listallnetworkservices',
                shell=True, 
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                raise Exception(f"macOS 어댑터 탐지 실패: {result.stderr}")
            
            lines = result.stdout.splitlines()
            logger.info(f"macOS 네트워크 서비스 목록: {lines}")
            
            # Wi-Fi를 우선적으로 선택
            for line in lines:
                if line and not line.startswith("*") and "Wi-Fi" in line:
                    adapter_name = line.strip()
                    logger.info(f"macOS Wi-Fi 어댑터 감지: {adapter_name}")
                    return adapter_name
            
            # Wi-Fi가 없으면 첫 번째 활성화된 어댑터 선택
            for line in lines:
                if line and not line.startswith("*"):
                    adapter_name = line.strip()
                    logger.info(f"macOS 어댑터 감지: {adapter_name}")
                    return adapter_name
            
            raise Exception("macOS 어댑터 이름을 찾을 수 없습니다.")
            
        except Exception as e:
            logger.error(f"macOS 어댑터 탐지 오류: {e}")
            raise
    
    @staticmethod
    def set_dns(dns_ip: str) -> bool:
        """DNS 서버 설정"""
        if not dns_ip:
            raise ValueError("DNS IP가 None입니다.")
        
        # IP 형식 유효성 검사
        try:
            DNSIpRequest(ip=dns_ip)
        except Exception as e:
            raise ValueError(f"유효하지 않은 IP 형식: {dns_ip}")
        
        # 관리자 권한 확인 제거 - 일반 사용자도 DNS 변경 가능하도록 수정
        # if not AdminChecker.is_admin():
        #     logger.warning("관리자 권한이 없습니다. DNS 설정을 위해 권한이 필요합니다.")
        #     raise Exception("DNS 설정을 위해 관리자 권한이 필요합니다.")
        
        os_name = platform.system()
        logger.info(f"DNS 설정 시작: {dns_ip} ({os_name})")
        
        try:
            if os_name == "Windows":
                adapter = DNSService.detect_adapter_win()
                # 현재 DNS가 동일하면 변경 생략 (OS 권한 팝업 최소화)
                current = DNSService.get_current_dns()
                if current and current.strip() == dns_ip.strip():
                    logger.info(f"현재 DNS가 이미 {dns_ip} 이므로 변경을 생략합니다.")
                    return True
                command = f'netsh interface ip set dns name="{adapter}" static {dns_ip}'
                
            elif os_name == "Darwin":  # macOS
                adapter = DNSService.detect_adapter_mac()
                command = f'networksetup -setdnsservers "{adapter}" {dns_ip}'
                
            elif os_name == "Linux":  # Linux
                # Linux에서는 /etc/resolv.conf 파일을 직접 수정
                command = f'echo "nameserver {dns_ip}" | sudo tee /etc/resolv.conf'
                
            else:
                raise Exception("Windows, macOS, Linux만 지원합니다.")
            
            logger.info(f"실행 명령어: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                timeout=30
            )
            def _dec(b):
                return (b.decode('cp949', errors='ignore') if isinstance(b, (bytes, bytearray)) else b) or ''
            stdout = _dec(result.stdout)
            stderr = _dec(result.stderr)
            
            logger.info(f"명령어 실행 결과 - returncode: {result.returncode}")
            logger.info(f"stdout: {stdout}")
            logger.info(f"stderr: {stderr}")
            
            if result.returncode != 0:
                # 권한 부족 메시지면 UAC로 명령만 승격 실행 (원래 창 유지)
                if ('권한 상승' in (stdout + stderr)) or ('elevation' in (stdout + stderr).lower()) or ('access is denied' in (stdout + stderr).lower()):
                    exit_code = DNSService._run_elevated_netsh(f'interface ip set dns name="{adapter}" static {dns_ip}')
                    if exit_code != 0:
                        raise Exception("DNS 설정 실패(승격 시도 후)")
                else:
                    error_msg = f"DNS 설정 실패: {stderr.strip()}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
            
            logger.info(f"DNS 설정 성공: {dns_ip}")
            return True
            
        except subprocess.TimeoutExpired:
            error_msg = "DNS 설정 명령어 실행 시간 초과"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"DNS 설정 중 오류: {e}")
            raise
    
    @staticmethod
    def reset_dns() -> bool:
        """DNS 서버 리셋 (기본값으로 복구)"""
        # 관리자 권한 확인 제거 - 일반 사용자도 DNS 리셋 가능하도록 수정
        # if not AdminChecker.is_admin():
        #     logger.warning("관리자 권한이 없습니다. DNS 리셋을 위해 권한이 필요합니다.")
        #     raise Exception("DNS 리셋을 위해 관리자 권한이 필요합니다.")
        
        os_name = platform.system()
        logger.info(f"DNS 리셋 시작 ({os_name})")
        
        try:
            if os_name == "Windows":
                adapter = DNSService.detect_adapter_win()
                command = f'netsh interface ip set dns name="{adapter}" dhcp'
                
            elif os_name == "Darwin":  # macOS
                adapter = DNSService.detect_adapter_mac()
                command = f'networksetup -setdnsservers "{adapter}" Empty'
                
            elif os_name == "Linux":  # Linux
                # Linux에서는 기본 DNS로 복구 (systemd-resolved 사용)
                command = 'sudo systemctl restart systemd-resolved'
                
            else:
                raise Exception("Windows, macOS, Linux만 지원합니다.")
            
            logger.info(f"실행 명령어: {command}")
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True
            )
            def _dec(b):
                return (b.decode('cp949', errors='ignore') if isinstance(b, (bytes, bytearray)) else b) or ''
            stdout = _dec(result.stdout)
            stderr = _dec(result.stderr)
            
            if result.returncode != 0:
                if ('권한 상승' in (stdout + stderr)) or ('elevation' in (stdout + stderr).lower()) or ('access is denied' in (stdout + stderr).lower()):
                    exit_code = DNSService._run_elevated_netsh(f'interface ip set dns name="{adapter}" dhcp')
                    if exit_code != 0:
                        raise Exception("DNS 리셋 실패(승격 시도 후)")
                else:
                    error_msg = f"DNS 리셋 실패: {stderr.strip()}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
            
            logger.info("DNS 리셋 성공")
            return True
            
        except Exception as e:
            logger.error(f"DNS 리셋 중 오류: {e}")
            raise

    @staticmethod
    def _run_elevated_netsh(arguments: str) -> int:
        """UAC로 netsh만 승격 실행하여 원래 창을 유지. 종료코드 반환."""
        try:
            SHELLEXECUTEINFOW = ctypes.c_buffer
            ShellExecuteEx = ctypes.windll.shell32.ShellExecuteExW
            SEE_MASK_NOCLOSEPROCESS = 0x00000040
            class SHELLEXECUTEINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.c_ulong),
                    ("fMask", ctypes.c_ulong),
                    ("hwnd", ctypes.c_void_p),
                    ("lpVerb", ctypes.c_wchar_p),
                    ("lpFile", ctypes.c_wchar_p),
                    ("lpParameters", ctypes.c_wchar_p),
                    ("lpDirectory", ctypes.c_wchar_p),
                    ("nShow", ctypes.c_int),
                    ("hInstApp", ctypes.c_void_p),
                    ("lpIDList", ctypes.c_void_p),
                    ("lpClass", ctypes.c_wchar_p),
                    ("hkeyClass", ctypes.c_void_p),
                    ("dwHotKey", ctypes.c_ulong),
                    ("hIcon", ctypes.c_void_p),
                    ("hProcess", ctypes.c_void_p),
                ]
            info = SHELLEXECUTEINFO()
            info.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
            info.fMask = SEE_MASK_NOCLOSEPROCESS
            info.hwnd = None
            info.lpVerb = "runas"
            info.lpFile = "netsh"
            info.lpParameters = arguments
            info.lpDirectory = None
            info.nShow = 1
            if not ShellExecuteEx(ctypes.byref(info)):
                return 1
            # 대기 및 종료코드 확인
            kernel32 = ctypes.windll.kernel32
            kernel32.WaitForSingleObject(info.hProcess, 60_000)
            exit_code = ctypes.c_ulong()
            if kernel32.GetExitCodeProcess(info.hProcess, ctypes.byref(exit_code)) == 0:
                return 1
            return int(exit_code.value)
        except Exception:
            return 1
    
    @staticmethod
    def get_current_dns() -> Optional[str]:
        """현재 DNS 서버 확인"""
        os_name = platform.system()
        
        try:
            if os_name == "Windows":
                # nslookup 출력에서 Address 라인을 우선적으로 파싱 (해석된 DNS IP)
                proc = subprocess.run(
                    'nslookup google.com',
                    shell=True,
                    capture_output=True
                )
                def _dec(b):
                    return (b.decode('cp949', errors='ignore') if isinstance(b, (bytes, bytearray)) else b) or ''
                out = _dec(proc.stdout)
                # 예: Address:  8.8.8.8 또는 Addresses: 8.8.8.8
                for line in out.splitlines():
                    m = re.search(r'Address(?:es)?:\s*([0-9]{1,3}(?:\.[0-9]{1,3}){3})', line)
                    if m:
                        return m.group(1)
                # 보조: Server 라인이 도메인명일 수 있어 IP가 없으면 None
                        
            elif os_name == "Darwin":
                result = subprocess.run(
                    'scutil --dns | grep nameserver',
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                if result.stdout:
                    return result.stdout.splitlines()[0].split()[-1]
            
            return None
            
        except Exception as e:
            logger.error(f"현재 DNS 확인 중 오류: {e}")
            return None
