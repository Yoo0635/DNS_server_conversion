#!/usr/bin/env python3
"""
Network Performance Optimizer - 간단한 실행 스크립트
PyQt5 메인 스레드에서 모든 것을 실행
"""

import sys
import os
import threading
import time
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
    except Exception as e:
        print(f"포트 정리 중 오류 (무시 가능): {e}")

def start_backend_in_thread():
    """백엔드 서버를 별도 스레드에서 시작"""
    try:
        # 백엔드 서버 import 및 실행
        os.chdir(backend_path)
        
        import uvicorn
        from main import app
        
        print("🚀 백엔드 서버 시작 중...")
        uvicorn.run(app, host="127.0.0.1", port=9002, log_level="info")
    except Exception as e:
        print(f"❌ 백엔드 서버 시작 실패: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🌐 Network Performance Optimizer v3.1.0 - 간단한 실행 모드")
    print("=" * 60)

    # 포트 정리
    cleanup_ports()

    # 백엔드 서버를 별도 스레드에서 시작
    backend_thread = threading.Thread(target=start_backend_in_thread, daemon=True)
    backend_thread.start()

    # 백엔드 서버가 시작될 때까지 대기
    print("⏳ 백엔드 서버 시작 대기 중...")
    time.sleep(3)

    # 프론트엔드 GUI 시작 (메인 스레드에서)
    try:
        os.chdir(frontend_path)
        from PyQt5.QtWidgets import QApplication
        from pyqt_app import MainWindow
        
        print("🖥️ 프론트엔드 GUI 시작 중...")
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        
        print("✅ 애플리케이션이 성공적으로 시작되었습니다!")
        print("🔄 종료하려면 창을 닫으세요")
        print("-" * 60)
        
        # GUI 이벤트 루프 시작 (메인 스레드에서)
        return app.exec_()
        
    except Exception as e:
        print(f"❌ 프론트엔드 GUI 시작 실패: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(0 if exit_code else 1)
    except KeyboardInterrupt:
        print("\n🔄 사용자가 프로그램을 종료합니다...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
