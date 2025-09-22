@echo off
REM Network Optimizer - Windows용 빌드 스크립트

echo 🌐 Network Optimizer v2.0.1 - Windows 빌드
echo ==========================================

REM Python 버전 확인
echo 🐍 Python 버전 확인...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되지 않았거나 PATH에 없습니다.
    pause
    exit /b 1
)

REM PyInstaller 설치 확인 및 설치
echo 📦 PyInstaller 설치 확인...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller가 설치되지 않았습니다. 설치 중...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ PyInstaller 설치 실패
        pause
        exit /b 1
    )
) else (
    echo ✅ PyInstaller가 이미 설치되어 있습니다.
)

REM 의존성 설치
echo 📚 의존성 설치...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 의존성 설치 실패
    pause
    exit /b 1
)

REM 빌드 디렉토리 정리
echo 🧹 이전 빌드 파일 정리...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Windows용 빌드 실행
echo 🪟 Windows용 빌드 중...
pyinstaller --clean NetworkOptimizer.spec
if %errorlevel% neq 0 (
    echo ❌ 빌드 실패
    pause
    exit /b 1
)

echo.
echo 🎉 빌드 완료!
echo 📁 빌드 결과: dist/ 폴더를 확인하세요
echo.
echo 🚀 실행 방법:
echo    Windows: dist\NetworkOptimizer.exe 더블클릭
echo.
pause

