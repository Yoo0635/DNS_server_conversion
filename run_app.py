#!/usr/bin/env python3
"""
Network Performance Optimizer - 메인 실행 스크립트
백엔드와 프론트엔드를 동시에 실행
"""

import sys
import os
import subprocess
import time
import threading
from pathlib import Path

def start_backend():
    """백엔드 서버 시작"""
    try:
        backend_path = Path(__file__).parent / "backend"
        os.chdir(backend_path)
        subprocess.run([sys.executable, "main.py"], check=True)
    except Exception as e:
        print(f"백엔드 시작 실패: {e}")

def start_frontend():
    """프론트엔드 시작"""
    try:
        # 백엔드가 시작될 때까지 잠시 대기
        time.sleep(3)
        
        frontend_path = Path(__file__).parent / "frontend"
        os.chdir(frontend_path)
        subprocess.run([sys.executable, "pyqt_app.py"], check=True)
    except Exception as e:
        print(f"프론트엔드 시작 실패: {e}")

def main():
    """메인 실행 함수"""
    print("🌐 Network Performance Optimizer v3.1.0")
    print("=====================================")
    print("🚀 백엔드와 프론트엔드를 시작합니다...")
    
    # 백엔드를 별도 스레드에서 시작
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # 프론트엔드 시작
    start_frontend()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🔄 사용자가 프로그램을 종료합니다...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
