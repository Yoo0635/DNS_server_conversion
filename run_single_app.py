#!/usr/bin/env python3
"""
Network Performance Optimizer - 단일 프로세스 실행 스크립트
백엔드와 프론트엔드를 하나의 프로세스에서 실행
"""

import sys
import os
import threading
import time
import signal
import subprocess
from pathlib import Path

# PyInstaller 환경에서 경로 처리
if getattr(sys, 'frozen', False):
    # 실행 파일인 경우
    bundle_dir = Path(sys._MEIPASS)
    backend_path = bundle_dir / "backend"
    frontend_path = bundle_dir / "frontend"
else:
    # 개발 환경인 경우
    current_dir = Path(__file__).parent
    backend_path = current_dir / "backend"
    frontend_path = current_dir / "frontend"

# sys.path에 경로 추가
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(frontend_path))

def cleanup_ports():
    """포트 정리"""
    try:
        # 포트 9002 정리
        result = subprocess.run(['lsof', '-ti:9002'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    subprocess.run(['kill', '-9', pid], capture_output=True)
        
        # 포트 9001 정리 (혹시 모를 경우)
        result = subprocess.run(['lsof', '-ti:9001'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                if pid:
                    subprocess.run(['kill', '-9', pid], capture_output=True)
    except Exception as e:
        print(f"포트 정리 중 오류 (무시 가능): {e}")

def start_backend_server():
    """백엔드 서버를 별도 스레드에서 시작"""
    try:
        # 백엔드 서버 import 및 실행
        os.chdir(backend_path)
        
        # FastAPI 관련 모듈들을 미리 import
        import fastapi
        import uvicorn
        import uvicorn.lifespan
        import uvicorn.protocols
        import uvicorn.loops
        
        from main import app
        
        print("🚀 백엔드 서버 시작 중...")
        uvicorn.run(app, host="127.0.0.1", port=9002, log_level="info")
    except Exception as e:
        print(f"❌ 백엔드 서버 시작 실패: {e}")
        import traceback
        traceback.print_exc()

def start_frontend_gui():
    """프론트엔드 GUI 시작"""
    try:
        os.chdir(frontend_path)
        from PyQt5.QtWidgets import QApplication
        from pyqt_app import MainWindow
        
        print("🖥️ 프론트엔드 GUI 시작 중...")
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"❌ 프론트엔드 GUI 시작 실패: {e}")
        import traceback
        traceback.print_exc()

def cleanup_processes():
    """프로세스 정리 (단일 프로세스에서는 스레드 종료)"""
    print("🔄 애플리케이션 종료 중...")
    # Uvicorn 서버 종료 시그널 보내기
    # 이 부분은 uvicorn.run이 블로킹 호출이므로, 스레드 종료 시 자동으로 정리됨
    # PyQt 앱 종료 시 sys.exit(app.exec_())가 호출되므로, 이 스레드도 종료됨
    print("✅ 모든 프로세스가 종료되었습니다.")

def main():
    print("🌐 Network Performance Optimizer v3.0.0 - 단일 프로세스 모드")
    print("=" * 60)

    # 기존 포트 정리 (혹시 모를 잔여 프로세스)
    cleanup_ports()

    backend_thread = threading.Thread(target=start_backend_server)
    frontend_thread = threading.Thread(target=start_frontend_gui)

    backend_thread.start()
    time.sleep(5) # 백엔드 서버가 완전히 시작될 때까지 충분히 대기
    frontend_thread.start()

    print("✅ 애플리케이션이 성공적으로 시작되었습니다!")
    print("🔄 종료하려면 창을 닫거나 Ctrl+C를 누르세요")
    print("-" * 60)

    try:
        while frontend_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔄 사용자가 프로그램을 종료합니다...")
    finally:
        cleanup_processes()
        # 스레드가 완전히 종료될 때까지 대기
        if backend_thread.is_alive():
            # Uvicorn 서버를 강제로 종료하는 방법이 필요할 수 있음
            # 여기서는 간단히 스레드 종료를 기다림
            pass
        backend_thread.join(timeout=5)
        frontend_thread.join(timeout=5)
        sys.exit(0)

if __name__ == "__main__":
    main()
