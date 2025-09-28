# Network Optimizer v3.1.0 - 크로스 플랫폼 빌드 가이드 (개선된 버전)

이 문서는 Network Optimizer v3.1.0을 Windows, macOS, Linux에서 빌드하는 방법을 안내합니다.

## ✨ v3.1.0 새로운 기능
- **즉시 표시되는 스플래시 화면**: 앱 더블클릭 시 즉시 로딩 화면 표시
- **실제 백엔드 상태 확인**: 고정된 3초 대기 → 실제 백엔드 상태 확인 (최대 8초)
- **최적화된 시작 시간**: 더 빠른 앱 시작
- **향상된 사용자 경험**: 로딩 진행 상황 실시간 표시, 예상 시간 안내

## 📋 사전 요구사항

### 공통 요구사항
- Python 3.8 이상
- pip (Python 패키지 관리자)
- 인터넷 연결 (의존성 다운로드용)

### 플랫폼별 요구사항
- **Windows**: Windows 10 이상
- **macOS**: macOS 10.13 이상
- **Linux**: Ubuntu 18.04 이상 또는 동등한 배포판

## 🔨 빌드 방법

### 1. macOS에서 빌드

```bash
# macOS용 빌드 (개선된 버전)
./build_macos_v3_improved.sh
```

**생성되는 파일:**
- `dist/NetworkOptimizer-macOS.app` (macOS 앱 번들)
- 즉시 스플래시 화면과 실제 진행률 표시 기능 포함

### 2. Windows에서 빌드

```batch
REM Windows용 빌드 (개선된 버전)
build_windows_v3.bat
```

**생성되는 파일:**
- `dist/NetworkOptimizer-Windows/` (Windows 실행 파일 폴더)
- `dist/NetworkOptimizer-Windows.exe` (Windows 실행 파일)
- 즉시 스플래시 화면과 실제 진행률 표시 기능 포함

### 3. Linux에서 빌드

```bash
# Linux용 빌드 (개선된 버전)
./build_linux_v3.sh
```

**생성되는 파일:**
- `dist/NetworkOptimizer-Linux/` (Linux 실행 파일 폴더)
- `dist/NetworkOptimizer-Linux` (Linux 실행 파일)
- 즉시 스플래시 화면과 실제 진행률 표시 기능 포함

## 📦 배포용 파일 준비

### macOS 배포
```bash
# 압축 파일 생성
zip -r "NetworkOptimizer-macOS-v3.0.0.zip" "dist/NetworkOptimizer-macOS.app"
```

### Windows 배포
```batch
REM 압축 파일 생성 (7-Zip 또는 WinRAR 필요)
"C:\Program Files\7-Zip\7z.exe" a "NetworkOptimizer-Windows-v3.0.0.zip" "dist\NetworkOptimizer-Windows\"
```

### Linux 배포
```bash
# 압축 파일 생성
tar -czf "NetworkOptimizer-Linux-v3.0.0.tar.gz" -C dist NetworkOptimizer-Linux/
```

## 🚀 실행 방법

### macOS
```bash
# 더블클릭으로 실행하거나
open dist/NetworkOptimizer-macOS.app

# 터미널에서 실행
./dist/NetworkOptimizer-macOS.app/Contents/MacOS/NetworkOptimizer-macOS
```

### Windows
```batch
REM 더블클릭으로 실행하거나
dist\NetworkOptimizer-Windows.exe

REM 또는 폴더 내 실행 파일 실행
dist\NetworkOptimizer-Windows\NetworkOptimizer-Windows.exe
```

### Linux
```bash
# 실행 권한 부여
chmod +x dist/NetworkOptimizer-Linux

# 실행
./dist/NetworkOptimizer-Linux
```

## ✨ 주요 특징

- **완전 독립 실행**: Python 설치가 필요 없습니다
- **안정적인 단일 프로세스**: 백엔드와 프론트엔드가 하나의 프로세스에서 실행
- **크로스 플랫폼**: Windows, macOS, Linux 모두 지원
- **DNS 기능 완전 지원**: 모든 플랫폼에서 DNS 설정, 측정, 리셋 기능
- **GUI 완전 지원**: PyQt5 기반의 사용자 친화적인 GUI

## 🛠️ 문제 해결

### 빌드 실패 시
1. Python 버전 확인: `python --version` 또는 `python3 --version`
2. 의존성 재설치: `pip install -r requirements.txt`
3. PyInstaller 재설치: `pip install --upgrade PyInstaller`
4. 이전 빌드 파일 정리: `rm -rf build dist` (Linux/macOS) 또는 `rmdir /s build dist` (Windows)

### 실행 실패 시
1. 관리자 권한으로 실행 (DNS 설정 시)
2. 방화벽 설정 확인
3. 포트 충돌 확인 (9002 포트 사용)
4. 바이러스 백신 소프트웨어 예외 설정

## 📁 파일 구조

```
Network-Project-Restored/
├── backend/                 # 백엔드 소스 코드
├── frontend/                # 프론트엔드 소스 코드
├── run_instant_splash.py    # 즉시 스플래시 화면 실행 스크립트 (v3.1.0)
├── run_single_app.py        # 단일 프로세스 실행 스크립트 (이전 버전)
├── NetworkOptimizer-*.spec  # 각 플랫폼별 PyInstaller 설정
├── build_*_v3.sh           # 각 플랫폼별 빌드 스크립트
├── build_*_v3.bat          # Windows용 빌드 스크립트
├── requirements.txt         # Python 의존성
└── README.md               # 프로젝트 설명
```

## 🎯 GitHub Releases 업로드

각 플랫폼별 빌드 완료 후:

1. **macOS**: `NetworkOptimizer-macOS-v3.1.0.zip`
2. **Windows**: `NetworkOptimizer-Windows-v3.1.0.zip`
3. **Linux**: `NetworkOptimizer-Linux-v3.1.0.tar.gz`

이 파일들을 GitHub Releases에 업로드하여 사용자들이 다운로드할 수 있도록 합니다.

---

**Network Optimizer 팀 v3.1.0** 🚀
