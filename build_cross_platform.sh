#!/bin/bash

# Network Optimizer - 크로스 플랫폼 빌드 스크립트
# Windows, macOS, Linux 모두 지원

echo "🌐 Network Optimizer v2.0.1 - 크로스 플랫폼 빌드"
echo "================================================"

# 현재 플랫폼 감지
PLATFORM=$(uname -s)
echo "🔍 현재 플랫폼: $PLATFORM"

# Python 버전 확인
echo "🐍 Python 버전 확인..."
python3 --version

# PyInstaller 설치 확인 및 설치
echo "📦 PyInstaller 설치 확인..."
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller가 설치되지 않았습니다. 설치 중..."
    pip3 install pyinstaller
else
    echo "✅ PyInstaller가 이미 설치되어 있습니다."
fi

# 의존성 설치
echo "📚 의존성 설치..."
pip3 install -r requirements.txt

# 빌드 디렉토리 정리
echo "🧹 이전 빌드 파일 정리..."
rm -rf build/
rm -rf dist/

# 플랫폼별 빌드 실행
echo "🔨 빌드 시작..."

case $PLATFORM in
    "Darwin")
        echo "🍎 macOS용 빌드 중..."
        pyinstaller --clean NetworkOptimizer.spec
        echo "✅ macOS용 .app 파일이 생성되었습니다: dist/NetworkOptimizer.app"
        ;;
    "Linux")
        echo "🐧 Linux용 빌드 중..."
        pyinstaller --clean NetworkOptimizer.spec
        echo "✅ Linux용 실행 파일이 생성되었습니다: dist/NetworkOptimizer"
        ;;
    "CYGWIN"*|"MINGW"*|"MSYS"*)
        echo "🪟 Windows용 빌드 중..."
        pyinstaller --clean NetworkOptimizer.spec
        echo "✅ Windows용 실행 파일이 생성되었습니다: dist/NetworkOptimizer.exe"
        ;;
    *)
        echo "❌ 지원되지 않는 플랫폼입니다: $PLATFORM"
        exit 1
        ;;
esac

echo ""
echo "🎉 빌드 완료!"
echo "📁 빌드 결과: dist/ 폴더를 확인하세요"
echo ""
echo "🚀 실행 방법:"
case $PLATFORM in
    "Darwin")
        echo "   macOS: dist/NetworkOptimizer.app 더블클릭 또는"
        echo "         open dist/NetworkOptimizer.app"
        ;;
    "Linux")
        echo "   Linux: ./dist/NetworkOptimizer"
        ;;
    "CYGWIN"*|"MINGW"*|"MSYS"*)
        echo "   Windows: dist/NetworkOptimizer.exe 더블클릭"
        ;;
esac

