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