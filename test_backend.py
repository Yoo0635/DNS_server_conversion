#!/usr/bin/env python3
"""
백엔드 서버 테스트 스크립트
"""

import sys
import os
import subprocess

def test_backend():
    """백엔드 서버 테스트"""
    print("🔍 백엔드 서버 테스트 시작...")
    
    # 백엔드 디렉토리로 이동
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    if not os.path.exists(backend_dir):
        print("❌ 백엔드 디렉토리를 찾을 수 없습니다.")
        return False
    
    print(f"📁 백엔드 디렉토리: {backend_dir}")
    
    # Python 파일들 확인
    main_py = os.path.join(backend_dir, 'main.py')
    mydns_py = os.path.join(backend_dir, 'mydns.py')
    ip_py = os.path.join(backend_dir, 'ip.py')
    
    print(f"📄 main.py 존재: {os.path.exists(main_py)}")
    print(f"📄 mydns.py 존재: {os.path.exists(mydns_py)}")
    print(f"📄 ip.py 존재: {os.path.exists(ip_py)}")
    
    # 백엔드 디렉토리에서 직접 실행
    try:
        print("🚀 백엔드 서버를 시작합니다...")
        print("📍 서버 주소: http://127.0.0.1:8000")
        print("🔄 종료하려면 Ctrl+C를 누르세요")
        print("-" * 50)
        
        # uvicorn으로 서버 시작
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ], cwd=backend_dir)
        
    except KeyboardInterrupt:
        print("\n🛑 서버가 중지되었습니다.")
    except Exception as e:
        print(f"❌ 서버 시작 실패: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_backend()

