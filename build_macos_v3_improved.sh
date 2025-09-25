#!/bin/bash

# Network Optimizer v3.1.0 - 개선된 macOS용 빌드 스크립트
# 로딩 시간 최적화 및 스플래시 화면 추가

VERSION="3.1.0"
APP_NAME="NetworkOptimizer-macOS"
SPEC_FILE="NetworkOptimizer-macOS.spec"

echo "🌐 $APP_NAME v$VERSION - 개선된 macOS용 빌드"
echo "============================================"
echo "✨ 새로운 기능:"
echo "   - 즉시 표시되는 스플래시 화면"
echo "   - 실제 백엔드 상태 확인"
echo "   - 최적화된 시작 시간"
echo "   - 향상된 사용자 경험"
echo ""

# 현재 플랫폼 확인 (macOS에서만 실행)
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "⚠️ 이 스크립트는 macOS에서만 실행할 수 있습니다."
    echo "   현재 OS: $OSTYPE"
    echo "   macOS에서 실행해주세요."
    exit 1
fi

echo "🍎 macOS 환경 확인 완료"

# Python 버전 확인
echo "🐍 Python 버전 확인..."
PYTHON_CMD="python3"
if ! command -v $PYTHON_CMD &> /dev/null
then
    echo "❌ Python 3가 설치되어 있지 않습니다. 설치해주세요."
    exit 1
fi
echo "$($PYTHON_CMD --version)"

# PyInstaller 설치 확인
echo "📦 PyInstaller 설치 확인..."
if ! $PYTHON_CMD -m PyInstaller --version &> /dev/null
then
    echo "⚠️ PyInstaller가 설치되어 있지 않습니다. 설치합니다..."
    $PYTHON_CMD -m pip install PyInstaller
    if [ $? -ne 0 ]; then
        echo "❌ PyInstaller 설치 실패."
        exit 1
    fi
    echo "✅ PyInstaller 설치 완료."
else
    echo "✅ PyInstaller가 이미 설치되어 있습니다."
fi

# 의존성 설치
echo "📚 의존성 설치..."
$PYTHON_CMD -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 의존성 설치 실패."
    exit 1
fi

# 이전 빌드 파일 정리
echo "🧹 이전 빌드 파일 정리..."
rm -rf build dist

echo "🔨 개선된 macOS용 빌드 중..."

# PyInstaller 실행
$PYTHON_CMD -m PyInstaller "$SPEC_FILE" --noconfirm
if [ $? -ne 0 ]; then
    echo "❌ macOS 빌드 실패."
    exit 1
fi

echo ""
echo "🎉 개선된 macOS 빌드 완료!"
echo "📁 빌드 결과: dist/ 폴더를 확인하세요"
echo ""
echo "📦 생성된 파일:"
echo "   - dist/$APP_NAME.app (macOS 앱 번들)"
echo ""
echo "🚀 사용 방법:"
echo "   1. dist/$APP_NAME.app 더블클릭"
echo "   2. 또는 터미널: open dist/$APP_NAME.app"
echo ""
echo "✨ 개선된 특징:"
echo "   - 즉시 표시되는 스플래시 화면"
echo "   - 실제 백엔드 상태 확인 (3초 → 최대 8초)"
echo "   - 최적화된 시작 시간"
echo "   - 향상된 사용자 경험"
echo "   - 완전 독립 실행 (Python 설치 불필요)"
echo "   - 안정적인 단일 프로세스"
echo "   - 모든 DNS 기능 지원"
echo "   - macOS 네이티브 .app 번들"
echo ""
echo "🎯 사용자 경험 개선:"
echo "   - 앱 더블클릭 시 즉시 스플래시 화면 표시"
echo "   - 로딩 진행 상황 실시간 표시"
echo "   - 예상 시간 안내"
echo "   - 혼란 최소화"
echo ""

