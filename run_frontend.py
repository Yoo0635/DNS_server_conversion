#!/usr/bin/env python3
"""
프론트엔드 애플리케이션 실행 스크립트
Network Performance Optimizer GUI를 시작합니다.
"""

import sys
import os
import platform

def check_dependencies():
    """필수 의존성 확인"""
    try:
        import tkinter
        import matplotlib
        import requests
        print("✅ 모든 의존성이 설치되어 있습니다.")
        return True
    except ImportError as e:
        print(f"❌ 의존성 누락: {e}")
        print("다음 명령어로 의존성을 설치하세요:")
        print("pip install -r requirements.txt")
        return False

def check_backend():
    """백엔드 서버 연결 확인"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if response.status_code == 200:
            print("✅ 백엔드 서버에 연결되었습니다.")
            return True
    except:
        pass
    
    print("⚠️  백엔드 서버에 연결할 수 없습니다.")
    print("백엔드 서버를 먼저 시작하세요:")
    print("python run_backend.py")
    return False

def start_frontend():
    """프론트엔드 애플리케이션 시작"""
    print("🖥️  Network Performance Optimizer GUI를 시작합니다...")
    print("=" * 50)
    
    try:
        # 프론트엔드 모듈 import
        from frontend.main_ui import main
        main()
    except ImportError as e:
        print(f"❌ 프론트엔드 모듈 로딩 실패: {e}")
        print("프로젝트 구조를 확인하세요.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 애플리케이션 시작 실패: {e}")
        sys.exit(1)

def main():
    """메인 함수"""
    print("🌐 Network Performance Optimizer - Frontend Application")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    # 백엔드 연결 확인 (선택사항)
    if not check_backend():
        response = input("백엔드 없이 계속하시겠습니까? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    start_frontend()

if __name__ == "__main__":
    main()

