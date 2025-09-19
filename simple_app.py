#!/usr/bin/env python3
"""
Network Performance Optimizer - 백엔드 포함 실행 파일
"""

import sys
import os
import subprocess
import threading
import time
import signal
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

class NetworkOptimizerApp:
    """네트워크 성능 최적화 통합 애플리케이션"""
    
    def __init__(self):
        self.backend_process = None
        self.running = True
        
    def start_backend(self):
        """백엔드 서버 시작"""
        print("🚀 백엔드 서버를 시작합니다...")
        
        try:
            # 실행 파일인지 확인
            if getattr(sys, 'frozen', False):
                # PyInstaller로 실행된 경우
                backend_dir = Path(sys._MEIPASS) / "backend"
            else:
                # 개발 환경인 경우
                backend_dir = Path(__file__).parent / "backend"
            
            if not backend_dir.exists():
                print("❌ 백엔드 디렉토리를 찾을 수 없습니다.")
                print(f"찾는 경로: {backend_dir}")
                return False
            
            # uvicorn으로 서버 시작
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "main:app", 
                "--host", "127.0.0.1", 
                "--port", "9001",
                "--log-level", "error"
            ], cwd=backend_dir)
            
            print("✅ 백엔드 서버가 성공적으로 시작되었습니다.")
            return True
                
        except Exception as e:
            print(f"❌ 백엔드 서버 시작 중 오류: {e}")
            return False
    
    def wait_for_backend(self):
        """백엔드 서버가 준비될 때까지 대기"""
        import requests
        max_attempts = 30
        for i in range(max_attempts):
            try:
                response = requests.get("http://127.0.0.1:9001/health", timeout=1)
                if response.status_code == 200:
                    print("✅ 백엔드 서버 연결 확인 완료")
                    return True
            except:
                pass
            time.sleep(1)
        print("❌ 백엔드 서버 연결 시간 초과")
        return False
    
    def cleanup(self):
        """정리 작업"""
        if self.backend_process:
            print("✅ 백엔드 서버가 종료되었습니다.")
            self.backend_process.terminate()
            self.backend_process.wait()
    
    def signal_handler(self, signum, frame):
        """시그널 핸들러"""
        print("\n🛑 애플리케이션을 종료합니다...")
        self.running = False
        self.cleanup()
        sys.exit(0)

def main():
    """메인 실행 함수"""
    print("🌐 Network Performance Optimizer")
    print("=" * 50)
    print("✅ 애플리케이션을 시작합니다...")
    
    app = NetworkOptimizerApp()
    
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, app.signal_handler)
    signal.signal(signal.SIGTERM, app.signal_handler)
    
    try:
        # 백엔드 시작 시도
        backend_started = app.start_backend()
        
        if backend_started:
            # 백엔드 준비 대기
            if app.wait_for_backend():
                print("🎉 서비스 시작 중입니다...")
                print("📱 GUI 창이 곧 열립니다...")
                print("🔄 종료하려면 Ctrl+C를 누르세요")
                print("-" * 50)
            else:
                print("⚠️ 백엔드 서버 연결 실패")
                print("📱 GUI만 실행합니다 (측정 기능 제한)")
                print("-" * 50)
        else:
            print("⚠️ 백엔드 서버 시작 실패")
            print("📱 GUI만 실행합니다 (측정 기능 제한)")
            print("-" * 50)
        
        # PyQt5 프론트엔드 실행 (백엔드 상태와 관계없이)
        from frontend.pyqt_app import main as frontend_main
        frontend_main()
        
    except ImportError as e:
        print(f"❌ 모듈 로딩 실패: {e}")
        print("개발 환경에서 실행하세요:")
        print("python run_app.py")
        print("5초 후 자동 종료...")
        time.sleep(5)
    except Exception as e:
        print(f"❌ 실행 오류: {e}")
        print("5초 후 자동 종료...")
        time.sleep(5)
    finally:
        app.cleanup()

if __name__ == "__main__":
    main()
