#!/usr/bin/env python3
"""
Network Performance Optimizer - 원클릭 실행 스크립트
가상환경 확인, 의존성 설치, 애플리케이션 실행을 모두 자동화합니다.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description, use_venv=True):
    """명령어 실행"""
    print(f"🔄 {description}...")
    
    if use_venv:
        # 가상환경의 Python 사용
        system = platform.system()
        if system == "Windows":
            python_path = "venv\\Scripts\\python"
        else:
            python_path = "venv/bin/python"
        
        if not Path(python_path).exists():
            print(f"❌ 가상환경을 찾을 수 없습니다. 먼저 setup.py를 실행하세요.")
            return False
        
        command = command.replace("python", python_path)
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} 완료")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 실패: {e}")
        return False

def check_and_install_dependencies():
    """의존성 확인 및 설치"""
    system = platform.system()
    if system == "Windows":
        pip_path = "venv\\Scripts\\pip"
    else:
        pip_path = "venv/bin/pip"
    
    if not Path(pip_path).exists():
        print("❌ 가상환경이 없습니다. setup.py를 먼저 실행하세요.")
        return False
    
    # 의존성 설치
    return run_command(f"{pip_path} install -r requirements.txt", "의존성 설치", use_venv=False)

def main():
    """메인 함수"""
    print("🚀 Network Performance Optimizer - 원클릭 실행")
    print("=" * 50)
    
    # 가상환경 확인
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ 가상환경이 없습니다.")
        print("다음 명령어로 먼저 설정하세요:")
        print("python setup.py")
        sys.exit(1)
    
    # 의존성 확인 및 설치
    if not check_and_install_dependencies():
        print("❌ 의존성 설치 실패")
        sys.exit(1)
    
    print("\n🎉 모든 준비가 완료되었습니다!")
    print("🚀 애플리케이션을 시작합니다...")
    print("=" * 50)
    
    # 애플리케이션 실행
    if not run_command("python run_app.py", "애플리케이션 실행"):
        print("❌ 애플리케이션 실행 실패")
        sys.exit(1)

if __name__ == "__main__":
    main()

