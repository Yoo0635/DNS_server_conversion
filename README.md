# 🌐 Network Performance Optimizer v1.0.0

네트워크 성능 최적화를 위한 DNS 및 IP 응답 속도 측정 도구입니다.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Yoo0635/Network-Project)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/Yoo0635/Network-Project)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/Yoo0635/Network-Project)

## ✨ 주요 기능

- **DNS 서버 성능 측정**: Google, KT, SKB, LGU+, KISA DNS 서버별 응답 시간 비교
- **IP 주소 성능 측정**: 도메인의 여러 IP 주소 중 가장 빠른 IP 찾기
- **실시간 시각화**: 현대적인 그래프로 성능 데이터 시각화
- **DNS 서버 설정**: 최적의 DNS 서버로 자동 변경
- **크로스 플랫폼 지원**: Windows, macOS, Linux 지원
- **플랫폼별 권한 관리**: Windows UAC, macOS 비밀번호 입력
- **종합 분석**: DNS와 IP 성능을 종합한 최적화 추천

## 🚀 빠른 시작

### 1. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

#### 🚀 간편 실행 (추천!)

**실행 파일 다운로드 후 더블클릭:**
```
1. GitHub에서 ZIP 파일 다운로드
2. 압축 해제
3. dist/NetworkOptimizer.app 더블클릭 (macOS)
```

#### 🔧 개발자용 실행

**하나의 명령어로 백엔드와 프론트엔드를 동시에 실행:**

```bash
python run_app.py
```

**프론트엔드만 실행:**
```bash
python run_frontend.py
```

## 📁 프로젝트 구조

```
Network-Project/
├── backend/                 # FastAPI 백엔드
│   ├── main.py             # 메인 API 서버
│   ├── admin_check.py      # 관리자 권한 체크
│   ├── routers/            # API 라우터
│   ├── services/           # 비즈니스 로직
│   ├── schemas/            # 데이터 모델
│   └── dns_servers.py      # DNS 서버 목록
├── frontend/               # PyQt5 프론트엔드
│   ├── pyqt_app.py         # 메인 애플리케이션
│   ├── pyqt_window.py      # 메인 윈도우
│   ├── pyqt_charts.py      # 그래프 생성
│   └── api_client.py       # API 클라이언트
├── run_app.py              # 통합 실행 스크립트
├── run_frontend.py         # 프론트엔드 실행 스크립트
└── requirements.txt        # 전체 의존성
```

## 🔧 API 엔드포인트

### DNS 성능 측정
```
GET /api/v1/measure?domain=example.com&count=5
```

### IP 성능 측정
```
GET /api/v1/ip?domain=example.com
```

### DNS 서버 설정
```
POST /api/v1/apply
Content-Type: application/json
{"server_name": "Google"}
```

### DNS 서버 리셋
```
POST /api/v1/reset
```

### 서버 상태 확인
```
GET /health
```

### API 문서
```
http://127.0.0.1:9001/docs
```

## 🎨 UI 특징

- **현대적인 PyQt5 디자인**: 플랫폼별 네이티브 스타일 적용
- **반응형 레이아웃**: 다양한 화면 크기 지원
- **실시간 피드백**: 측정 진행 상황 및 결과 표시
- **직관적인 인터페이스**: 사용하기 쉬운 버튼과 입력 필드
- **관리자 권한 표시**: DNS 설정 가능 여부 실시간 표시
- **플랫폼별 권한 요청**: Windows UAC, macOS 비밀번호 입력

## 📊 측정 결과

측정 결과는 CSV 파일로 자동 저장됩니다:

- `dns_응답속도_결과.csv`: DNS 서버별 응답 시간
- `ip_응답속도_결과.csv`: IP 주소별 응답 시간

## 🖥️ 시스템 요구사항

- **Python**: 3.8 이상
- **운영체제**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **메모리**: 최소 512MB RAM
- **네트워크**: 인터넷 연결 필요

## 🔍 사용법

1. **도메인 입력**: 측정하고 싶은 도메인 주소 입력
2. **측정 횟수 선택**: DNS 측정 횟수 설정 (1-20회)
3. **측정 시작**: 원하는 측정 유형 선택
   - 🔍 DNS 서버 응답 시간 측정
   - ⚡ IP 응답 속도 측정
   - 📊 종합 성능 분석
4. **DNS 설정**: 최적의 DNS 서버로 변경
   - Windows: UAC 팝업에서 "예" 클릭
   - macOS: 비밀번호 입력 다이얼로그
5. **결과 확인**: 그래프로 성능 데이터 시각화

## 🛠️ 개발자 정보

이 프로젝트는 네트워크 성능 최적화를 위한 교육 및 연구 목적으로 개발되었습니다.

### 기술 스택

- **Backend**: FastAPI, Python, dnspython, Pydantic
- **Frontend**: PyQt5, Matplotlib
- **Data**: Pandas, NumPy
- **Visualization**: Matplotlib
- **Architecture**: MVC 패턴, RESTful API

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

버그 리포트나 기능 제안은 이슈로 등록해 주세요.

---

**Network Performance Optimizer** - 최적의 네트워크 경로를 찾아보세요! 🚀
