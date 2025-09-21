#!/bin/bash
# Network Performance Optimizer - 자동 릴리스 스크립트

set -e

VERSION=$1
if [ -z "$VERSION" ]; then
    echo "❌ 버전을 지정해주세요!"
    echo "사용법: ./release.sh v2.0.1"
    exit 1
fi

echo "🚀 Network Performance Optimizer $VERSION 릴리스 준비 중..."
echo "================================================"

# 현재 상태 확인
echo "📋 현재 상태 확인..."
git status --porcelain
if [ $? -ne 0 ]; then
    echo "❌ Git 저장소가 아닙니다!"
    exit 1
fi

# 빌드 실행
echo "🏗️ 빌드 실행 중..."
./build_improved.sh

# 릴리스 디렉토리 생성
echo "📁 릴리스 디렉토리 준비..."
mkdir -p releases
cd releases

# 압축 파일 생성
echo "📦 압축 파일 생성 중..."

# macOS 앱
if [ -d "../dist/NetworkOptimizer.app" ]; then
    echo "  - macOS 앱 압축 중..."
    zip -r "NetworkOptimizer-macOS-$VERSION.zip" ../dist/NetworkOptimizer.app
    echo "  ✅ NetworkOptimizer-macOS-$VERSION.zip 생성 완료"
fi

# Linux/Unix 실행 파일
if [ -d "../dist/NetworkOptimizer" ]; then
    echo "  - Linux/Unix 실행 파일 압축 중..."
    tar -czf "NetworkOptimizer-Linux-$VERSION.tar.gz" -C ../dist NetworkOptimizer
    echo "  ✅ NetworkOptimizer-Linux-$VERSION.tar.gz 생성 완료"
fi

# 파일 크기 확인
echo "📊 생성된 파일들:"
ls -lh *.zip *.tar.gz 2>/dev/null || echo "압축 파일이 생성되지 않았습니다."

cd ..

echo ""
echo "🎉 릴리스 준비 완료!"
echo "================================================"
echo "📋 다음 단계:"
echo "1. Git 태그 생성:"
echo "   git tag -a $VERSION -m \"Release $VERSION\""
echo "   git push origin $VERSION"
echo ""
echo "2. GitHub Releases에서 다음 파일들을 업로드:"
for file in releases/*.zip releases/*.tar.gz; do
    if [ -f "$file" ]; then
        echo "   - $(basename $file)"
    fi
done
echo ""
echo "3. 릴리스 노트 작성 (CHANGELOG.md 참조)"
echo ""
echo "🔗 GitHub Releases URL:"
echo "https://github.com/Yoo0635/Network-Project/releases"
echo ""
echo "📝 릴리스 노트 예시:"
echo "## Network Performance Optimizer $VERSION"
echo ""
echo "### 새로운 기능"
echo "- PyQt5 기반 GUI 인터페이스"
echo "- 실시간 네트워크 트래픽 모니터링"
echo "- DNS 서버 상태 확인"
echo "- 스마트 티켓팅 시스템"
echo ""
echo "### 시스템 요구사항"
echo "- macOS 10.14+ 또는 Linux"
echo "- Python 3.8+ (소스 코드 실행 시)"
echo ""
echo "### 설치 방법"
echo "1. 다운로드한 압축 파일을 원하는 위치에 압축 해제"
echo "2. 실행 파일을 더블클릭하여 실행"