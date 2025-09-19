import platform
import subprocess
import getpass
import ctypes
import sys
import os

class AdminChecker:
    """플랫폼별 관리자 권한 체크 및 요청 클래스"""
    
    @staticmethod
    def is_admin():
        """현재 관리자 권한 여부 확인"""
        platform_name = platform.system()
        
        if platform_name == "Windows":
            return AdminChecker._is_admin_windows()
        elif platform_name == "Darwin":  # macOS
            return AdminChecker._is_admin_macos()
        else:  # Linux
            return AdminChecker._is_admin_linux()
    
    @staticmethod
    def _is_admin_windows():
        """Windows 관리자 권한 확인"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    @staticmethod
    def _is_admin_macos():
        """macOS 관리자 권한 확인"""
        try:
            # sudo 권한 테스트
            result = subprocess.run(['sudo', '-n', 'true'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    @staticmethod
    def _is_admin_linux():
        """Linux 관리자 권한 확인"""
        try:
            return os.geteuid() == 0
        except:
            return False
    
    @staticmethod
    def request_admin():
        """플랫폼별 관리자 권한 요청"""
        platform_name = platform.system()
        
        if platform_name == "Windows":
            return AdminChecker._request_admin_windows()
        elif platform_name == "Darwin":
            return AdminChecker._request_admin_macos()
        else:
            return AdminChecker._request_admin_linux()
    
    @staticmethod
    def _request_admin_windows():
        """Windows UAC 팝업으로 관리자 권한 요청"""
        try:
            # UAC 팝업으로 관리자 권한 요청
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            return True
        except Exception as e:
            print(f"Windows 관리자 권한 요청 실패: {e}")
            return False
    
    @staticmethod
    def _request_admin_macos():
        """macOS 비밀번호 입력으로 관리자 권한 요청"""
        try:
            print("\n🔐 DNS 설정을 위해 관리자 비밀번호가 필요합니다.")
            print("터미널에 비밀번호를 입력해주세요. (입력한 비밀번호는 화면에 표시되지 않습니다)")
            
            password = getpass.getpass("관리자 비밀번호: ")
            
            # sudo 권한으로 명령어 실행 테스트
            result = subprocess.run(['sudo', '-S', 'true'], 
                                  input=password, text=True, 
                                  capture_output=True)
            
            if result.returncode == 0:
                print("✅ 관리자 권한 확인됨")
                return True
            else:
                print("❌ 비밀번호가 올바르지 않습니다.")
                return False
                
        except Exception as e:
            print(f"macOS 관리자 권한 요청 실패: {e}")
            return False
    
    @staticmethod
    def _request_admin_linux():
        """Linux sudo 권한 요청"""
        try:
            print("\n🔐 DNS 설정을 위해 sudo 권한이 필요합니다.")
            print("터미널에 비밀번호를 입력해주세요.")
            
            password = getpass.getpass("sudo 비밀번호: ")
            
            # sudo 권한으로 명령어 실행 테스트
            result = subprocess.run(['sudo', '-S', 'true'], 
                                  input=password, text=True, 
                                  capture_output=True)
            
            if result.returncode == 0:
                print("✅ sudo 권한 확인됨")
                return True
            else:
                print("❌ 비밀번호가 올바르지 않습니다.")
                return False
                
        except Exception as e:
            print(f"Linux sudo 권한 요청 실패: {e}")
            return False
    
    @staticmethod
    def show_permission_guide():
        """플랫폼별 권한 요청 가이드 표시"""
        platform_name = platform.system()
        
        if platform_name == "Windows":
            guide = """
🔐 Windows 관리자 권한 요청

1. Windows 보안 팝업이 나타납니다
2. '예'를 클릭하여 관리자 권한을 허용하세요
3. 프로그램이 관리자 권한으로 재시작됩니다

⚠️ 주의: 이 프로그램은 안전한 DNS 서버만 사용합니다
"""
        elif platform_name == "Darwin":
            guide = """
🔐 macOS 관리자 권한 요청

1. 터미널에 관리자 비밀번호를 입력하세요
2. 비밀번호는 화면에 표시되지 않습니다
3. 입력 후 Enter를 누르세요

⚠️ 주의: 이 프로그램은 안전한 DNS 서버만 사용합니다
"""
        else:
            guide = """
🔐 Linux sudo 권한 요청

1. 터미널에 sudo 비밀번호를 입력하세요
2. 비밀번호는 화면에 표시되지 않습니다
3. 입력 후 Enter를 누르세요

⚠️ 주의: 이 프로그램은 안전한 DNS 서버만 사용합니다
"""
        
        print(guide)
    
    @staticmethod
    def check_and_request_admin():
        """관리자 권한 확인 및 요청"""
        if AdminChecker.is_admin():
            print("✅ 관리자 권한 확인됨")
            return True
        
        print("❌ 관리자 권한이 필요합니다.")
        AdminChecker.show_permission_guide()
        
        return AdminChecker.request_admin()
