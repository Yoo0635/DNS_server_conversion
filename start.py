<<<<<<< HEAD
import subprocess
import sys
import threading
import os
import time

def run_backend():
    # 백엔드 서버 실행
    os.chdir('backend')
    subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1'])
    # subprocess.run()은 서브프로세스를 실행합니다.
    # sys.executable은 현재 파이썬 인터프리터 경로를 자동으로 찾아줍니다.
    # '--host 127.0.0.1'은 로컬호스트로만 접속을 허용합니다.

def run_frontend():
    # 현재 작업 디렉터리를 프로젝트 루트로 되돌립니다.
    os.chdir('..')
    # 프론트엔드 UI 실행
    os.chdir('frontend')
    subprocess.run([sys.executable, 'ticket_ui.py'])

if __name__ == "__main__":
    # 백엔드를 별도의 스레드에서 실행
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # 백엔드가 완전히 실행될 시간을 벌기 위해 잠시 대기
    time.sleep(2)  

    # 프론트엔드 UI 실행
    run_frontend()
=======
#!/usr/bin/env python3
"""
Network Performance Optimizer - 간단 실행 스크립트
"""

import subprocess
import sys
import os

def main():
    """간단한 실행 함수"""
    print("🌐 Network Performance Optimizer 시작 중...")
    
    # run_app.py 실행
    try:
        subprocess.run([sys.executable, "run_app.py"])
    except KeyboardInterrupt:
        print("\n🛑 애플리케이션이 종료되었습니다.")
    except Exception as e:
        print(f"❌ 실행 오류: {e}")

if __name__ == "__main__":
    main()

>>>>>>> 2e01351 (tkinter기반)
