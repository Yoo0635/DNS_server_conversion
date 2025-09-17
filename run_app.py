#!/usr/bin/env python3
"""
Network Performance Optimizer - 통합 실행 스크립트
백엔드와 프론트엔드를 동시에 실행합니다.
"""

import sys
import os
import subprocess
import threading
import time
import platform
import signal
from pathlib import Path

class NetworkOptimizerApp:
    """네트워크 성능 최적화 통합 애플리케이션"""
    
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def check_dependencies(self):
        """필수 의존성 확인"""
        print("🔍 의존성 확인 중...")
        try:
            import fastapi
            import uvicorn
            import tkinter
            import matplotlib
            import requests
            import dns
            import pandas
            print("✅ 모든 의존성이 설치되어 있습니다.")
            return True
        except ImportError as e:
            print(f"❌ 의존성 누락: {e}")
            print("다음 명령어로 의존성을 설치하세요:")
            print("pip install -r requirements.txt")
            return False
    
    def start_backend(self):
        """백엔드 서버 시작"""
        print("🚀 백엔드 서버를 시작합니다...")
        
        try:
            # 백엔드 디렉토리로 이동
            backend_dir = Path(__file__).parent / "backend"
            if not backend_dir.exists():
                print("❌ 백엔드 디렉토리를 찾을 수 없습니다.")
                return False
            
            # uvicorn으로 서버 시작
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "main:app", 
                "--host", "127.0.0.1", 
                "--port", "9000", 
                "--reload"
            ], cwd=backend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 서버 시작 대기
            time.sleep(3)
            
            if self.backend_process.poll() is None:
                print("✅ 백엔드 서버가 성공적으로 시작되었습니다.")
                print("📍 API 주소: http://127.0.0.1:9000")
                return True
            else:
                print("❌ 백엔드 서버 시작 실패")
                return False
                
        except Exception as e:
            print(f"❌ 백엔드 서버 시작 중 오류: {e}")
            return False
    
    def start_frontend(self):
        """프론트엔드 애플리케이션 시작"""
        print("🖥️  프론트엔드 애플리케이션을 시작합니다...")
        
        try:
            # 프론트엔드 모듈 import 및 실행
            from frontend.main_ui import main
            main()
            
        except ImportError as e:
            print(f"❌ 프론트엔드 모듈 로딩 실패: {e}")
            return False
        except Exception as e:
            print(f"❌ 프론트엔드 시작 실패: {e}")
            return False
    
    def wait_for_backend(self):
        """백엔드 서버가 준비될 때까지 대기"""
        import requests
        max_attempts = 30
        for i in range(max_attempts):
            try:
                response = requests.get("http://127.0.0.1:9000/health", timeout=1)
                if response.status_code == 200:
                    print("✅ 백엔드 서버 연결 확인 완료")
                    return True
            except:
                pass
            time.sleep(1)
            print(f"⏳ 백엔드 서버 연결 대기 중... ({i+1}/{max_attempts})")
        
        print("❌ 백엔드 서버 연결 시간 초과")
        return False
    
    def cleanup(self):
        """리소스 정리"""
        print("\n🛑 애플리케이션을 종료합니다...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ 백엔드 서버가 종료되었습니다.")
            except:
                try:
                    self.backend_process.kill()
                    print("✅ 백엔드 서버가 강제 종료되었습니다.")
                except:
                    pass
        
        self.running = False
    
    def signal_handler(self, signum, frame):
        """시그널 핸들러"""
        self.cleanup()
        sys.exit(0)
    
    def run(self):
        """메인 실행 함수"""
        print("🌐 Network Performance Optimizer")
        print("=" * 50)
        
        # 의존성 확인
        if not self.check_dependencies():
            sys.exit(1)
        
        # 시그널 핸들러 등록
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # 백엔드 시작
            if not self.start_backend():
                print("❌ 백엔드 서버 시작 실패")
                sys.exit(1)
            
            # 백엔드 연결 대기
            if not self.wait_for_backend():
                print("❌ 백엔드 서버 연결 실패")
                self.cleanup()
                sys.exit(1)
            
            print("\n🎉 모든 서비스가 준비되었습니다!")
            print("📱 GUI 창이 곧 열립니다...")
            print("🔄 종료하려면 Ctrl+C를 누르세요")
            print("-" * 50)
            
            # 프론트엔드 시작 (메인 스레드에서)
            self.start_frontend()
            
        except KeyboardInterrupt:
            print("\n🛑 사용자에 의해 중단되었습니다.")
        except Exception as e:
            print(f"❌ 예상치 못한 오류: {e}")
        finally:
            self.cleanup()

def main():
    """메인 함수"""
    app = NetworkOptimizerApp()
    app.run()

if __name__ == "__main__":
    main()
