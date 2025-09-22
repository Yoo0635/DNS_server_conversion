@echo off
chcp 65001 > nul

REM Network Optimizer v3.0.0 - Windows용 빌드 스크립트

SET VERSION=3.0.0
SET APP_NAME=NetworkOptimizer-Windows
SET SPEC_FILE=NetworkOptimizer-Windows.spec

echo 🌐 %APP_NAME% v%VERSION% - Windows용 빌드
echo ================================================

echo 🔍 현재 플랫폼: Windows

REM Python 버전 확인
echo 🐍 Python 버전 확인...
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python이 설치되어 있지 않습니다. 설치해주세요.
    GOTO :EOF
)

REM PyInstaller 설치 확인
echo 📦 PyInstaller 설치 확인...
python -m PyInstaller --version > nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ⚠️ PyInstaller가 설치되어 있지 않습니다. 설치합니다...
    python -m pip install PyInstaller
    IF %ERRORLEVEL% NEQ 0 (
        echo ❌ PyInstaller 설치 실패.
        GOTO :EOF
    )
    echo ✅ PyInstaller 설치 완료.
) ELSE (
    echo ✅ PyInstaller가 이미 설치되어 있습니다.
)

REM 의존성 설치
echo 📚 의존성 설치...
python -m pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ 의존성 설치 실패.
    GOTO :EOF
)

REM 이전 빌드 파일 정리
echo 🧹 이전 빌드 파일 정리...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo 🔨 Windows용 빌드 중...

REM PyInstaller 실행
python -m PyInstaller "%SPEC_FILE%" --noconfirm
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Windows 빌드 실패.
    GOTO :EOF
)

echo.
echo 🎉 Windows 빌드 완료!
echo 📁 빌드 결과: dist\ 폴더를 확인하세요
echo.
echo 📦 생성된 파일:
echo    - dist\%APP_NAME%\ (Windows 실행 파일 폴더)
echo    - dist\%APP_NAME%.exe (Windows 실행 파일)
echo.
echo 🚀 사용 방법:
echo    1. Windows에서 dist\%APP_NAME%.exe 더블클릭
echo    2. 또는 dist\%APP_NAME%\ 폴더 전체를 Windows로 복사
echo.
echo ✨ 특징:
echo    - 완전 독립 실행 (Python 설치 불필요)
echo    - 안정적인 단일 프로세스
echo    - 모든 DNS 기능 지원
echo.
PAUSE
