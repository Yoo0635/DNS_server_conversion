#!/usr/bin/env python3
"""
Network Performance Optimizer - 메인 실행 스크립트
백엔드와 프론트엔드를 동시에 실행
"""

import sys
import os
import platform
import ctypes
import os
import subprocess
import time
import threading
from pathlib import Path
import logging
import tempfile

# ----------------------
# 단일 인스턴스 가드 (Windows 포함)
# ----------------------
_single_instance_acquired = False
def _acquire_single_instance_mutex() -> None:
    global _single_instance_acquired
    try:
        if platform.system() == "Windows":
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            CreateMutexW = kernel32.CreateMutexW
            CreateMutexW.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
            CreateMutexW.restype = wintypes.HANDLE
            # 세션 격리 이슈를 피하기 위해 Local 스코프 사용
            name = "Local\\NetworkOptimizer_SingleInstance_Mutex"
            handle = CreateMutexW(None, True, name)
            ERROR_ALREADY_EXISTS = 183
            last_error = ctypes.get_last_error()
            if last_error == ERROR_ALREADY_EXISTS:
                _show_message_box("Network Optimizer", "이미 실행 중입니다. 기존 창을 사용하세요.")
                sys.exit(0)
            _single_instance_acquired = True
        else:
            # 비 Windows는 간단 파일 락으로 대체(최소 구현)
            lock_path = Path(Path.home(), ".network_optimizer.lock")
            if lock_path.exists():
                _show_message_box("Network Optimizer", "이미 실행 중입니다. 기존 창을 사용하세요.")
                sys.exit(0)
            lock_path.write_text(str(os.getpid()))
            _single_instance_acquired = True
    except Exception:
        pass

_logger: logging.Logger

def _init_file_logger() -> logging.Logger:
    try:
        # 기존 logging 설정 초기화
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        # 새로운 logging 설정
        log_file = Path(tempfile.gettempdir()) / "NetworkOptimizer.log"
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # 파일 핸들러
        file_handler = logging.FileHandler(str(log_file), encoding="utf-8")
        file_handler.setFormatter(formatter)
        
        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # 루트 로거 설정
        logging.basicConfig(
            level=logging.INFO,
            handlers=[file_handler, console_handler],
            force=True  # 기존 설정 강제 덮어쓰기
        )
        
        logger = logging.getLogger("NetworkOptimizer")
        logger.info("==== Application start ====")
        return logger
    except Exception as e:
        print(f"Logger init failed: {e}")
        return logging.getLogger("noop")

def _show_message_box(title: str, message: str) -> None:
    try:
        if platform.system() == "Windows":
            ctypes.windll.user32.MessageBoxW(0, message, title, 0x00000040)
        else:
            print(f"{title}: {message}")
    except Exception:
        pass

def start_backend_uvicorn():
    """백엔드 서버를 현재 프로세스에서 스레드로 실행 (PyInstaller 재귀 방지)"""
    try:
        _logger.info("Starting backend (uvicorn thread)...")
        
        # PyInstaller 환경에서 모든 가능한 경로 추가
        if getattr(sys, 'frozen', False):
            # EXE 실행 시
            exe_dir = Path(sys.executable).parent
            meipass = getattr(sys, '_MEIPASS', None)
            
            paths_to_add = [
                exe_dir,
                exe_dir / "_internal",
                exe_dir / "backend",
                exe_dir / "_internal" / "backend" if (exe_dir / "_internal").exists() else None,
            ]
            
            if meipass:
                paths_to_add.extend([
                    Path(meipass),
                    Path(meipass) / "backend",
                ])
        else:
            # 소스 실행 시
            paths_to_add = [
                Path(__file__).parent,
                Path(__file__).parent / "backend",
            ]
        
        # 경로 추가
        for path in paths_to_add:
            if path and path.exists():
                sys.path.insert(0, str(path))
                _logger.info(f"Added to sys.path: {path}")
        
        # 백엔드 모듈 임포트 시도
        _logger.info("Attempting to import backend modules...")
        
        # 모든 필요한 모듈들 미리 임포트 (PyInstaller가 인식하도록)
        try:
            # DNS 관련
            import dns.resolver
            import dns.query
            import dns.rdatatype
            _logger.info("DNS modules imported successfully")
        except ImportError as e:
            _logger.warning(f"DNS modules import warning: {e}")
        
        try:
            # HTTP 관련
            import requests
            import urllib3
            _logger.info("HTTP modules imported successfully")
        except ImportError as e:
            _logger.warning(f"HTTP modules import warning: {e}")
        
        try:
            # PyQt 관련
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtCore import Qt
            _logger.info("PyQt modules imported successfully")
        except ImportError as e:
            _logger.warning(f"PyQt modules import warning: {e}")
        
        try:
            # Matplotlib 관련
            import matplotlib.pyplot as plt
            import matplotlib.backends.backend_qt5agg
            _logger.info("Matplotlib modules imported successfully")
        except ImportError as e:
            _logger.warning(f"Matplotlib modules import warning: {e}")
        
        # 직접 임포트 시도
        try:
            import backend.main
            _logger.info("Backend main import successful")
        except ImportError as e:
            _logger.error(f"Backend main import failed: {e}")
            raise Exception(f"백엔드 모듈을 찾을 수 없습니다: {e}")
        
        # uvicorn과 app 임포트
        import uvicorn
        from backend.main import app
        
        _logger.info("All backend imports successful")
        
        # uvicorn 서버 시작 (logging 설정 최소화)
        config = uvicorn.Config(
            app=app, 
            host="127.0.0.1", 
            port=9002, 
            reload=False, 
            log_level="warning",  # 로그 레벨 낮춤
            access_log=False,    # 액세스 로그 비활성화
            use_colors=False     # 색상 비활성화
        )
        server = uvicorn.Server(config)

        def _run():
            try:
                _logger.info("Starting uvicorn server...")
                server.run()
            except Exception as e:
                _logger.error(f"Uvicorn server error: {e}")

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        _logger.info("Backend thread started successfully")
        
    except Exception as e:
        _logger.exception("Backend start failed")
        _show_message_box("Network Optimizer - 오류", f"백엔드 시작 실패: {e}")
        raise  # 백엔드 실패 시 전체 앱 종료

def start_frontend_inprocess():
    """프론트엔드를 현재 프로세스에서 실행 (PyQt는 메인 스레드)"""
    try:
        _logger.info("Starting frontend (PyQt main)...")
        # 백엔드가 시작될 때까지 잠시 대기
        time.sleep(1.5)

        # PyInstaller 환경에서 모든 가능한 경로 추가
        if getattr(sys, 'frozen', False):
            # EXE 실행 시
            exe_dir = Path(sys.executable).parent
            meipass = getattr(sys, '_MEIPASS', None)
            
            paths_to_add = [
                exe_dir,
                exe_dir / "_internal",
                exe_dir / "frontend",
                exe_dir / "_internal" / "frontend" if (exe_dir / "_internal").exists() else None,
            ]
            
            if meipass:
                paths_to_add.extend([
                    Path(meipass),
                    Path(meipass) / "frontend",
                ])
        else:
            # 소스 실행 시
            paths_to_add = [
                Path(__file__).parent,
                Path(__file__).parent / "frontend",
            ]
        
        # 경로 추가
        for path in paths_to_add:
            if path and path.exists():
                sys.path.insert(0, str(path))
                _logger.info(f"Added to sys.path: {path}")
        
        # 프론트엔드 모듈 임포트 시도
        _logger.info("Attempting to import frontend modules...")
        
        # 직접 임포트 시도
        try:
            import frontend.pyqt_app
            _logger.info("Frontend pyqt_app import successful")
        except ImportError as e:
            _logger.error(f"Frontend pyqt_app import failed: {e}")
            raise Exception(f"프론트엔드 모듈을 찾을 수 없습니다: {e}")
        
        # 프론트엔드 실행
        from frontend.pyqt_app import main as frontend_main
        _logger.info("All frontend imports successful")
        
        rc = frontend_main()
        _logger.info("Frontend exited with code %s", rc)
        sys.exit(rc)
        
    except Exception as e:
        _logger.exception("Frontend start failed")
        _show_message_box("Network Optimizer - 오류", f"프론트엔드 시작 실패: {e}")
        raise  # 프론트엔드 실패 시 전체 앱 종료

def main():
    """메인 실행 함수"""
    # Windows: 관리자 권한 자동 승격 (최초 1회)
    # 빌드(EXE)에서는 PyInstaller --uac-admin으로 권한을 확보하고,
    # 소스 실행 시에는 자동 승격을 하지 않습니다(재실행 루프/폭주 방지)

    # Windows 콘솔(cp949 등) 환경에서도 안전하게 출력되도록 이모지 제거
    print("Network Performance Optimizer v3.1.0")
    print("=====================================")
    print("백엔드와 프론트엔드를 시작합니다...")
    
    # 로깅 초기화
    global _logger
    _logger = _init_file_logger()
    _logger.info("Main start")
    
    # Qt/Matplotlib 환경 변수 설정 (frozen 시 안정성 향상)
    os.environ.setdefault("QT_QPA_PLATFORM", "windows")
    os.environ.setdefault("MPLBACKEND", "QtAgg")

    # 단일 인스턴스 확보 (승격 후에만 시도)
    _acquire_single_instance_mutex()

    # 백엔드(Uvicorn)를 별도 스레드에서 시작
    start_backend_uvicorn()

    # 프론트엔드(PyQt) 시작 (메인 스레드)
    start_frontend_inprocess()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n사용자가 프로그램을 종료합니다...")
        sys.exit(0)
    except Exception as e:
        print(f"\n예상치 못한 오류: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
