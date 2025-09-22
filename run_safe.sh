#!/bin/bash

# Network Optimizer - 안전한 실행 스크립트
# 무한 창 생성 문제 해결

echo "🌐 Network Optimizer v2.0.1 - 안전 모드"
echo "========================================"

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# 기존 프로세스 정리
echo "🧹 기존 프로세스 정리 중..."
pkill -f "python3 main.py" 2>/dev/null || true
pkill -f "pyqt_app.py" 2>/dev/null || true
lsof -ti:9002 | xargs kill -9 2>/dev/null || true
lsof -ti:9001 | xargs kill -9 2>/dev/null || true

sleep 2

# 백엔드 시작 (백그라운드)
echo "🚀 백엔드 서버 시작 중..."
cd backend
python3 main.py &
BACKEND_PID=$!
echo "✅ 백엔드 서버 시작됨 (PID: $BACKEND_PID)"

# 백엔드가 완전히 시작될 때까지 대기
sleep 5

# 프론트엔드 시작 (단일 프로세스)
echo "🖥️ 프론트엔드 GUI 시작 중..."
cd ../frontend
python3 pyqt_app.py &
FRONTEND_PID=$!
echo "✅ 프론트엔드 GUI 시작됨 (PID: $FRONTEND_PID)"

echo ""
echo "🎉 애플리케이션이 성공적으로 시작되었습니다!"
echo "🔄 종료하려면 Ctrl+C를 누르세요"
echo "========================================"

# 종료 시그널 처리
cleanup() {
    echo ""
    echo "🔄 프로그램을 종료합니다..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    pkill -f "python3 main.py" 2>/dev/null || true
    pkill -f "pyqt_app.py" 2>/dev/null || true
    echo "✅ 모든 프로세스가 종료되었습니다."
    exit 0
}

# 시그널 트랩 설정
trap cleanup SIGINT SIGTERM

# 메인 프로세스 대기
wait

