#!/usr/bin/env python3
"""
백엔드 서버 실행 스크립트
Network Performance Optimizer API 서버를 시작합니다.
"""

import sys
import os
import subprocess
import platform

def check_dependencies():
    """필수 의존성 확인"""
    try:
        import fastapi
        import uvicorn
        import dns
        import pandas
        print("✅ 모든 의존성이 설치되어 있습니다.")
        return True
    except ImportError as e:
        print(f"❌ 의존성 누락: {e}")
        print("다음 명령어로 의존성을 설치하세요:")
        print("pip install -r requirements.txt")
        return False

def start_backend():
    """백엔드 서버 시작"""
    print("🚀 Network Performance Optimizer API 서버를 시작합니다...")
    print("📍 서버 주소: http://127.0.0.1:8000")
    print("📖 API 문서: http://127.0.0.1:8000/docs")
    print("🔄 서버를 중지하려면 Ctrl+C를 누르세요")
    print("-" * 50)
    
    try:
        # 백엔드 디렉토리로 이동
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        if os.path.exists(backend_dir):
            os.chdir(backend_dir)
        
        # uvicorn으로 서버 시작
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 서버가 중지되었습니다.")
    except Exception as e:
        print(f"❌ 서버 시작 실패: {e}")

def main():
    """메인 함수"""
    print("🌐 Network Performance Optimizer - Backend Server")
    print("=" * 50)
    
    if not check_dependencies():
        sys.exit(1)
    
    start_backend()

if __name__ == "__main__":
    main()

