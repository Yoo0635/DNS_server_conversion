import platform
import subprocess
import logging
from typing import Optional
from schemas.dns_models import DNSIpRequest
from admin_check import AdminChecker

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DNSService:
    """DNS 설정 및 관리 서비스"""
    
    @staticmethod
    def detect_adapter_win() -> str:
        """Windows 네트워크 어댑터 탐지"""
        try:
            result = subprocess.run(
                'netsh interface show interface',
                shell=True, 
                capture_output=True, 
                text=True, 
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                raise Exception(f"Windows 어댑터 탐지 실패: {result.stderr}")
            
            lines = result.stdout.splitlines()
            for line in lines:
                if "Connected" in line or "연결됨" in line:
                    adapter_name = line.strip().split()[-1]
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
                text=True, 
                encoding="utf-8",
                timeout=30  # 30초 타임아웃 추가
            )
            
            logger.info(f"명령어 실행 결과 - returncode: {result.returncode}")
            logger.info(f"stdout: {result.stdout}")
            logger.info(f"stderr: {result.stderr}")
            
            if result.returncode != 0:
                error_msg = f"DNS 설정 실패: {result.stderr.strip()}"
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
                capture_output=True, 
                text=True, 
                encoding="utf-8"
            )
            
            if result.returncode != 0:
                error_msg = f"DNS 리셋 실패: {result.stderr.strip()}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            logger.info("DNS 리셋 성공")
            return True
            
        except Exception as e:
            logger.error(f"DNS 리셋 중 오류: {e}")
            raise
    
    @staticmethod
    def get_current_dns() -> Optional[str]:
        """현재 DNS 서버 확인"""
        os_name = platform.system()
        
        try:
            if os_name == "Windows":
                result = subprocess.run(
                    'nslookup google.com',
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8'
                )
                # Windows nslookup 결과에서 DNS 서버 추출
                lines = result.stdout.splitlines()
                for line in lines:
                    if "Server:" in line:
                        return line.split(":")[1].strip()
                        
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
