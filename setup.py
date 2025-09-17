#!/usr/bin/env python3
"""
Network Performance Optimizer - 초기 설정 스크립트
가상환경 생성, 의존성 설치, 애플리케이션 실행을 자동화합니다.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """명령어 실행 및 결과 출력"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 실패: {e}")
        if e.stdout:
            print(f"출력: {e.stdout}")
        if e.stderr:
            print(f"오류: {e.stderr}")
        return False

def check_python_version():
    """Python 버전 확인"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8 이상이 필요합니다. 현재 버전: {version.major}.{version.minor}")
        return False
    print(f"✅ Python 버전 확인: {version.major}.{version.minor}.{version.micro}")
    return True

def create_virtual_environment():
    """가상환경 생성"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ 가상환경이 이미 존재합니다.")
        return True
    
    return run_command(f"{sys.executable} -m venv venv", "가상환경 생성")

def get_activation_command():
    """플랫폼별 가상환경 활성화 명령어 반환"""
    system = platform.system()
    if system == "Windows":
        return "venv\\Scripts\\activate"
    else:  # macOS, Linux
        return "source venv/bin/activate"

def install_dependencies():
    """의존성 설치"""
    # 가상환경의 pip 사용
    system = platform.system()
    if system == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    return run_command(f"{pip_path} install -r requirements.txt", "의존성 설치")

def main():
    """메인 설정 함수"""
    print("🌐 Network Performance Optimizer - 초기 설정")
    print("=" * 50)
    
    # Python 버전 확인
    if not check_python_version():
        sys.exit(1)
    
    # 가상환경 생성
    if not create_virtual_environment():
        sys.exit(1)
    
    # 의존성 설치
    if not install_dependencies():
        sys.exit(1)
    
    print("\n🎉 설정이 완료되었습니다!")
    print("=" * 50)
    print("📋 다음 단계:")
    print(f"1. 가상환경 활성화: {get_activation_command()}")
    print("2. 애플리케이션 실행: python run_app.py")
    print("\n💡 또는 다음 명령어로 바로 실행할 수 있습니다:")
    
    system = platform.system()
    if system == "Windows":
        print("venv\\Scripts\\python run_app.py")
    else:
        print("venv/bin/python run_app.py")

if __name__ == "__main__":
    main()

