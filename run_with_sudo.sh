#!/bin/bash

# Network Optimizer - sudo로 실행하는 스크립트
# DNS apply 기능을 위해 관리자 권한이 필요합니다.

echo "🌐 Network Performance Optimizer v2.0.1"
echo "========================================"
echo ""
echo "⚠️  DNS apply 기능을 사용하려면 관리자 권한이 필요합니다."
echo "   이 스크립트는 sudo로 실행됩니다."
echo ""
echo "🔐 관리자 비밀번호를 입력해주세요..."
echo ""

# 현재 디렉토리로 이동
cd "$(dirname "$0")"

# sudo로 애플리케이션 실행
sudo python3 run_app.py
