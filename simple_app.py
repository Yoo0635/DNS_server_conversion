#!/usr/bin/env python3
"""
Network Performance Optimizer - 간단한 실행 파일
"""

import sys
import os
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def main():
    """메인 실행 함수"""
    print("🌐 Network Performance Optimizer")
    print("=" * 50)
    print("✅ 애플리케이션을 시작합니다...")
    
    try:
        # PyQt5 프론트엔드 실행
        from frontend.pyqt_app import main as frontend_main
        frontend_main()
    except ImportError as e:
        print(f"❌ 모듈 로딩 실패: {e}")
        print("개발 환경에서 실행하세요:")
        print("python run_app.py")
        input("Enter를 눌러 종료...")
    except Exception as e:
        print(f"❌ 실행 오류: {e}")
        input("Enter를 눌러 종료...")

if __name__ == "__main__":
    main()
