#!/usr/bin/env python3
"""
Network Performance Optimizer - 메인 실행 스크립트
"""

import sys
import os
from pathlib import Path

def main():
    print("🌐 Network Performance Optimizer v2.0.1")
    print("=" * 50)
    print("✅ 애플리케이션이 성공적으로 실행되었습니다!")
    print("📱 GUI 창이 곧 열립니다...")
    print("🔄 종료하려면 Ctrl+C를 누르세요")
    print("-" * 50)
    
    try:
        # 상위 디렉토리의 main.py 실행
        parent_dir = Path(__file__).parent.parent
        main_py_path = parent_dir / "main.py"
        
        if main_py_path.exists():
            # sys.path에 상위 디렉토리 추가
            sys.path.insert(0, str(parent_dir))
            
            # main.py의 MainApp 클래스 import 및 실행
            from main import MainApp
            from PyQt5.QtWidgets import QApplication
            
            app = QApplication(sys.argv)
            window = MainApp()
            window.show()
            sys.exit(app.exec_())
        else:
            print(f"❌ main.py 파일을 찾을 수 없습니다: {main_py_path}")
            print("프로젝트 구조를 확인해주세요.")
            
    except ImportError as e:
        print("❌ 필요한 모듈이 설치되지 않았습니다.")
        print(f"오류: {e}")
        print("다음 명령어로 설치하세요:")
        print("pip install PyQt5 matplotlib numpy")
    except Exception as e:
        print(f"❌ 실행 중 오류: {e}")

if __name__ == "__main__":
    main()