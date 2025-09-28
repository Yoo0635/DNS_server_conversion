#!/usr/bin/env python3
"""
Network Performance Optimizer - 메인 실행 스크립트
모듈화된 런처를 사용하여 애플리케이션 실행
"""

import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.launcher import NetworkOptimizerLauncher

def main():
    """메인 실행 함수"""
    launcher = NetworkOptimizerLauncher()
    return launcher.launch_application()

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
