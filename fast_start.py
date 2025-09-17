#!/usr/bin/env python3
"""
Network Performance Optimizer - 빠른 시작 스크립트
가상환경 없이 바로 실행 (개발/테스트용)
"""

import sys
import subprocess
import os

def install_minimal_dependencies():
    """최소한의 의존성만 설치"""
    print("⚡ 최소 의존성 설치 중...")
    
    minimal_packages = [
        "fastapi",
        "uvicorn", 
        "dnspython",
        "pandas",
        "matplotlib",
        "requests"
    ]
    
    for package in minimal_packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package} 설치 완료")
        except subprocess.CalledProcessError:
            print(f"⚠️  {package} 설치 실패 (이미 설치되어 있을 수 있음)")

def main():
    """메인 함수"""
    print("⚡ Network Performance Optimizer - 빠른 시작")
    print("=" * 50)
    print("⚠️  주의: 이 방법은 개발/테스트용입니다.")
    print("   프로덕션에서는 가상환경 사용을 권장합니다.")
    print("=" * 50)
    
    # 최소 의존성 설치
    install_minimal_dependencies()
    
    print("\n🚀 애플리케이션을 시작합니다...")
    
    # 애플리케이션 실행
    try:
        subprocess.run([sys.executable, "run_app.py"])
    except KeyboardInterrupt:
        print("\n🛑 애플리케이션이 종료되었습니다.")
    except Exception as e:
        print(f"❌ 실행 오류: {e}")

if __name__ == "__main__":
    main()

