#!/bin/bash
# Network Performance Optimizer - 개선된 빌드 스크립트
# PyInstaller로 앱을 빌드하고 테스트합니다.

set -e  # 오류 발생 시 스크립트 중단

echo "🚀 Network Performance Optimizer - 개선된 빌드 시작"
echo "================================================"

# 현재 디렉토리 확인
BUILD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$BUILD_DIR")"
echo "📁 빌드 디렉토리: $BUILD_DIR"
echo "📁 프로젝트 디렉토리: $PROJECT_DIR"
cd "$BUILD_DIR"

# Python 환경 확인
echo "🐍 Python 환경 확인..."
python3 --version
pip3 --version

# 의존성 설치
echo "📦 의존성 설치..."
pip3 install -r requirements.txt

# 기존 빌드 파일 정리
echo "🧹 기존 빌드 파일 정리..."
rm -rf build/
rm -rf dist/
rm -rf __pycache__/
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# PyInstaller 설치 확인
echo "🔧 PyInstaller 설치 확인..."
pip3 install pyinstaller

# 빌드 실행
echo "🏗️ PyInstaller로 빌드 시작..."
pyinstaller --clean NetworkOptimizer.spec

# 빌드 결과 확인
echo "✅ 빌드 완료 - 결과 확인..."
if [ -f "dist/NetworkOptimizer/NetworkOptimizer" ]; then
    echo "✅ 실행 파일 생성됨: dist/NetworkOptimizer/NetworkOptimizer"
    ls -la "dist/NetworkOptimizer/NetworkOptimizer"
else
    echo "❌ 실행 파일 생성 실패"
    exit 1
fi

if [ -f "dist/NetworkOptimizer.app/Contents/MacOS/NetworkOptimizer" ]; then
    echo "✅ macOS 앱 생성됨: dist/NetworkOptimizer.app"
    ls -la "dist/NetworkOptimizer.app/Contents/MacOS/NetworkOptimizer"
else
    echo "❌ macOS 앱 생성 실패"
fi

# 디버깅 스크립트를 빌드에 포함
echo "🔍 디버깅 스크립트 복사..."
cp debug_build.py dist/NetworkOptimizer/ 2>/dev/null || echo "debug_build.py 없음"
if [ -d "dist/NetworkOptimizer.app" ]; then
    cp debug_build.py "dist/NetworkOptimizer.app/Contents/MacOS/" 2>/dev/null || echo "debug_build.py 없음"
fi

# 빌드된 앱의 구조 확인
echo "📁 빌드된 앱 구조 확인..."
echo "Linux/Unix 버전:"
find dist/NetworkOptimizer -type f -name "*.py" | head -5
echo ""
echo "macOS 앱 버전:"
find dist/NetworkOptimizer.app -type f -name "*.py" | head -5

echo ""
echo "🎉 빌드 완료!"
echo "================================================"
echo "📱 테스트 방법:"
echo "1. Linux/Unix: ./dist/NetworkOptimizer/NetworkOptimizer"
echo "2. macOS: open dist/NetworkOptimizer.app"
echo "3. 디버깅: python3 dist/NetworkOptimizer/debug_build.py"
echo "================================================"