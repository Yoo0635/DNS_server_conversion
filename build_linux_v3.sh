#!/bin/bash

# Network Optimizer v3.0.0 - Linux용 빌드 스크립트

VERSION="3.0.0"
APP_NAME="NetworkOptimizer-Linux"
SPEC_FILE="NetworkOptimizer-Linux.spec"

echo "🌐 $APP_NAME v$VERSION - Linux용 빌드"
echo "============================================"

# 현재 플랫폼 확인 (Linux에서만 실행)
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "⚠️ 이 스크립트는 Linux에서만 실행할 수 있습니다."
    echo "   현재 OS: $OSTYPE"
    echo "   Linux에서 실행해주세요."
    exit 1
fi

echo "🐧 Linux 환경 확인 완료"

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

echo "🔨 Linux용 빌드 중..."

# PyInstaller 실행
$PYTHON_CMD -m PyInstaller "$SPEC_FILE" --noconfirm
if [ $? -ne 0 ]; then
    echo "❌ Linux 빌드 실패."
    exit 1
fi

# 실행 권한 부여
chmod +x "dist/$APP_NAME"

echo ""
echo "🎉 Linux 빌드 완료!"
echo "📁 빌드 결과: dist/ 폴더를 확인하세요"
echo ""
echo "📦 생성된 파일:"
echo "   - dist/$APP_NAME/ (Linux 실행 파일 폴더)"
echo "   - dist/$APP_NAME (Linux 실행 파일)"
echo ""
echo "🚀 사용 방법:"
echo "   1. ./dist/$APP_NAME 실행"
echo "   2. 또는 dist/$APP_NAME/ 폴더 전체를 Linux로 복사"
echo ""
echo "✨ 특징:"
echo "   - 완전 독립 실행 (Python 설치 불필요)"
echo "   - 안정적인 단일 프로세스"
echo "   - 모든 DNS 기능 지원"
echo "   - Linux 네이티브 지원"
echo ""
