# 🌐 Network Optimizer v2.0.1 - 배포 가이드

## 📋 개요
Network Optimizer는 DNS 성능 측정 및 최적화를 위한 크로스 플랫폼 애플리케이션입니다.

## 🖥️ 지원 플랫폼
- ✅ **Windows** (Windows 10/11)
- ✅ **macOS** (macOS 10.13+)
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+)

## 🚀 실행 방법

### macOS
```bash
# 방법 1: .app 파일 더블클릭
open dist/NetworkOptimizer.app

# 방법 2: 터미널에서 실행
dist/NetworkOptimizer.app/Contents/MacOS/NetworkOptimizer
```

### Windows
```bash
# 방법 1: .exe 파일 더블클릭
dist/NetworkOptimizer.exe

# 방법 2: 명령 프롬프트에서 실행
dist\NetworkOptimizer.exe
```

### Linux
```bash
# 실행 권한 부여
chmod +x dist/NetworkOptimizer

# 실행
./dist/NetworkOptimizer
```

## 🔧 빌드 방법

### 자동 빌드 (권장)
```bash
# macOS/Linux
./build_cross_platform.sh

# Windows
build_windows.bat
```

### 수동 빌드
```bash
# 1. PyInstaller 설치
pip install pyinstaller

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 빌드 실행
pyinstaller --clean NetworkOptimizer.spec
```

## 📦 주요 기능

### 1. DNS 성능 측정
- 다양한 DNS 서버 속도 비교
- Google, KT, SKB, LGU, KISA DNS 지원
- CSV 결과 파일 자동 저장

### 2. IP 최적화
- 가장 빠른 IP 주소 자동 탐지
- 실시간 응답 속도 측정

### 3. DNS 설정 변경
- 원클릭 DNS 서버 변경
- 크로스 플랫폼 DNS 설정 지원
- 관리자 권한 불필요 (일반 사용자 사용 가능)

### 4. 시각화
- 실시간 차트 및 그래프
- 성능 비교 시각화
- 사용자 친화적 GUI

## 🛠️ 기술 스택

### Backend
- **FastAPI**: 고성능 웹 API
- **uvicorn**: ASGI 서버
- **dnspython**: DNS 쿼리 처리
- **pandas**: 데이터 처리

### Frontend
- **PyQt5**: 크로스 플랫폼 GUI
- **matplotlib**: 차트 및 그래프

### 배포
- **PyInstaller**: 실행 파일 생성
- **크로스 플랫폼**: Windows, macOS, Linux 지원

## 📁 프로젝트 구조
```
Network-Project-Restored/
├── backend/                 # 백엔드 API 서버
│   ├── main.py             # FastAPI 메인 서버
│   ├── routers/            # API 라우터
│   ├── services/           # 비즈니스 로직
│   └── schemas/            # 데이터 모델
├── frontend/               # 프론트엔드 GUI
│   ├── pyqt_app.py        # PyQt5 메인 앱
│   ├── pyqt_window.py     # 메인 윈도우
│   ├── pyqt_charts.py     # 차트 컴포넌트
│   └── api_client.py      # API 클라이언트
├── dist/                   # 배포용 실행 파일
├── build_cross_platform.sh # 크로스 플랫폼 빌드 스크립트
├── build_windows.bat       # Windows 빌드 스크립트
└── NetworkOptimizer.spec   # PyInstaller 설정 파일
```

## 🔒 보안 및 권한

### DNS 설정 권한
- **Windows**: netsh 명령어 사용 (일반 사용자 권한)
- **macOS**: networksetup 명령어 사용 (일반 사용자 권한)
- **Linux**: /etc/resolv.conf 직접 수정 (sudo 권한 필요)

### 보안 고려사항
- 안전한 DNS 서버만 사용 (Google, KT, SKB, LGU, KISA)
- 로컬 네트워크 설정만 변경
- 외부 네트워크 연결 없음

## 🐛 문제 해결

### 일반적인 문제
1. **포트 충돌**: 9002 포트가 사용 중인 경우
   ```bash
   # macOS/Linux
   lsof -ti:9002 | xargs kill -9
   
   # Windows
   netstat -ano | findstr :9002
   taskkill /PID <PID> /F
   ```

2. **권한 오류**: DNS 설정 실패 시
   ```bash
   # Linux에서만 필요
   sudo ./dist/NetworkOptimizer
   ```

3. **의존성 오류**: Python 패키지 누락 시
   ```bash
   pip install -r requirements.txt
   ```

## 📞 지원
- **버전**: v2.0.1
- **빌드 날짜**: $(date)
- **플랫폼**: 크로스 플랫폼 (Windows, macOS, Linux)

## 📄 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

