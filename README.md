# 🚀 Network Performance Optimizer v3.1.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)](https://shields.io/)

**여러 DNS 서버와 IP의 응답 속도를 실시간으로 측정, 비교하고 클릭 한 번으로 최적의 네트워크 환경을 설정하는 크로스 플랫폼 데스크톱 애플리케이션입니다.**

---

## 📘 프로젝트 소개

**Network Performance Optimizer**는 **FastAPI** 백엔드와 **PyQt5** GUI 프론트엔드로 구성된 네트워크 최적화 도구입니다. 주요 DNS 서버(Google, KT, SKB 등)를 대상으로 도메인 질의 응답 시간을 정밀하게 비교·분석하고, **가장 빠른 DNS를 원클릭으로 시스템에 적용**할 수 있습니다. 또한 대상 도메인의 실제 IP 응답 속도를 TCP 연결 시간을 기준으로 측정하여 **Matplotlib 차트**로 시각화합니다.

Windows 환경에서는 **UAC(사용자 계정 컨트롤) 프롬프트를 자동으로 처리**하여, 관리자 권한이 필요한 DNS 변경 작업을 번거로운 수동 승인 없이 매끄럽게 진행할 수 있도록 사용자 경험을 개선했습니다.

## ✨ 주요 기능

- 🌍 **DNS 서버별 응답 시간 측정**: 여러 DNS 서버에 대한 쿼리 응답 시간을 밀리초(ms) 단위로 측정하고 비교 분석합니다. (결과는 CSV로 자동 저장)
- ⚡ **IP 응답 속도 측정**: 특정 도메인에 연결된 IP 주소들의 TCP Port 80 연결 시간을 측정하여 실제 서버 도달 시간을 파악합니다.
- 🧠 **최적 서버 자동 식별**: 측정 결과를 바탕으로 가장 빠른 DNS 서버와 IP 주소를 자동으로 식별하여 요약 정보를 제공합니다.
- 🔧 **원클릭 DNS 적용/리셋**: 클릭 한 번으로 시스템의 DNS 설정을 가장 빠른 서버로 변경하거나, OS 기본값으로 손쉽게 복원합니다. (Windows/macOS/Linux 지원)
- 📊 **실시간 데이터 시각화**: **PyQt5**와 **Matplotlib**을 연동하여 측정된 DNS 및 IP 응답 속도를 실시간 막대그래프로 시각화합니다.
- 🔐 **Windows UAC 자동 처리**: DNS 변경 시 필요한 관리자 권한을 자동으로 요청하고 처리하여 사용자 편의성을 극대화했습니다.

## 🛠️ 기술 스택

| 구분 | 기술 | 설명 |
| :--- | :--- | :--- |
| **Backend** | `FastAPI`, `Uvicorn` | 비동기 웹 프레임워크 기반의 고성능 API 서버 |
| **Frontend** | `PyQt5`, `Matplotlib` | 크로스 플랫폼 GUI 및 데이터 시각화 |
| **Network** | `dnspython`, `socket` | DNS 쿼리 및 TCP 소켓 통신 |
| **Packaging** | `PyInstaller` | Python 애플리케이션을 단일 실행 파일(.exe)로 빌드 |
| **CI/CD** | `Shell Script`, `Batch Script`| 각 OS에 맞는 자동화된 빌드 스크립트 |

## 📦 설치 및 실행 방법

###  Prerequisites

- **Python 3.8 이상**이 설치되어 있어야 합니다.
- **포트 9002**가 사용 가능해야 합니다. (충돌 시 해당 포트를 비워주세요)

### 🪟 Windows (권장)

1.  `Releases` 탭에서 `NetworkOptimizer-Windows.exe` 파일을 다운로드합니다.
2.  파일을 더블클릭하여 실행합니다.
3.  UAC(사용자 계정 컨트롤) 팝업이 나타나면 **‘예’**를 클릭하여 관리자 권한을 허용합니다.

### 🍎 macOS / 🐧 Linux (소스 코드 실행)

가상 환경 구성을 권장합니다.

```bash
# 1. 프로젝트 클론
git clone [https://github.com/your-repo/NetworkPerformanceOptimizer.git](https://github.com/your-repo/NetworkPerformanceOptimizer.git)
cd NetworkPerformanceOptimizer

# 2. 가상 환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 애플리케이션 실행
python run_app.py
```

### ⚙️ 개발 서버만 별도 실행 (선택)
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 9002 --reload
```
---

### **3. 사용 시나리오, 폴더 구조**

## 🧪 사용 시나리오

1.  **GUI 실행**: 애플리케이션을 실행하고 측정할 도메인(예: `google.com`)을 입력합니다.
2.  **DNS 측정**: `DNS Server Response Time` 버튼을 클릭하여 각 DNS 서버의 응답 속도를 차트로 확인합니다.
3.  **DNS 적용**: 결과에서 가장 빠른 서버를 확인한 후, `Apply DNS` 버튼을 클릭하여 시스템에 즉시 적용합니다.
4.  **DNS 리셋**: 문제가 발생하거나 기본 설정으로 돌아가고 싶다면 `Reset DNS` 버튼을 클릭합니다.
5.  **IP 속도 확인**: `IP Response Speed Test` 버튼을 클릭하여 해당 도메인의 실제 서버별 연결 속도를 비교합니다.

## 🗂️ 폴더 구조

```plaintext
.
├── backend/
│   ├── main.py           # FastAPI 앱 엔트리, 라우터 등록
│   ├── routers/
│   │   ├── dns_measure.py  # GET /api/v1/measure (DNS 응답 시간)
│   │   ├── ip_measure.py   # GET /api/v1/ip (IP 응답 시간)
│   │   ├── dns_apply.py    # POST /api/v1/apply (DNS 적용)
│   │   └── dns_reset.py    # POST /api/v1/reset (DNS 리셋)
│   ├── services/
│   │   └── dns_service.py  # OS별 DNS 적용/리셋/어댑터 탐지 로직
│   ├── schemas/
│   │   └── dns_models.py   # Pydantic 데이터 모델 (검증/응답 스키마)
│   ├── dns_servers.py      # 지원 DNS 서버 목록
│   └── admin_check.py      # (보조) 관리자 권한 체크 유틸
├── frontend/
│   ├── pyqt_app.py         # PyQt5 앱 엔트리
│   ├── pyqt_window.py      # 메인 윈도우 UI 및 이벤트 핸들러
│   ├── pyqt_charts.py      # Matplotlib 차트 컴포넌트
│   └── api_client.py       # 백엔드 API 클라이언트
├── run_app.py              # 백엔드(스레드) + 프론트엔드(메인) 통합 실행
├── requirements.txt        # Python 의존성 목록
└── build_*.sh/.bat         # 각 OS별 빌드 스크립트
```
---

### **4. API 엔드포인트, 핵심 로직 상세**


## 🔌 주요 API 엔드포인트

| Method | Endpoint | 파라미터 / Body | 설명 |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | - | 프로젝트 소개 및 API 엔드포인트 안내 |
| `GET` | `/health` | - | 서버 상태 헬스 체크 |
| `GET` | `/api/v1/measure` | `domain`, `count` | 지정된 도메인의 DNS 응답 시간 측정 |
| `GET` | `/api/v1/ip` | `domain` | 지정된 도메인의 IP 응답 시간 측정 |
| `POST` | `/api/v1/apply` | `{"name": "<DNS_이름>"}` | 특정 DNS를 시스템에 적용 |
| `POST` | `/api/v1/reset` | - | 시스템 DNS 설정을 기본값으로 복원 |

## 🧠 핵심 로직 상세

<details>
<summary><strong>1. DNS 응답 시간 측정 (routers/dns_measure.py)</strong></summary>

-   **핵심 로직**
    -   입력된 `domain`을 Pydantic 모델(`DomainRequest`)로 검증합니다.
    -   `dns.resolver.Resolver` 객체를 사용하여 각 DNS 서버 IP를 `nameserver`로 지정합니다.
    -   지정된 서버에 `A` 레코드 쿼리를 `count`회 만큼 보내 응답 시간을 측정합니다.
    -   측정된 시간(ms)을 바탕으로 **평균/최소/최대** 값을 계산하고, 가장 빠른 서버와 느린 서버를 식별합니다.
    -   결과를 CSV 파일로 저장하고, `MeasureResponse` 모델에 담아 반환합니다.

-   **코드 조각**
    ```python
    # (요약) 각 DNS 서버에 대해 count번 질의하여 ms 단위 측정
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [server_ip]
    start_time = time.perf_counter()
    resolver.resolve(validated_domain, 'A')
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    ```

</details>

<details>
<summary><strong>2. IP 응답 속도 측정 (routers/ip_measure.py)</strong></summary>

-   **핵심 로직**
    -   `socket.gethostbyname_ex`를 통해 도메인에 연결된 모든 IPv4 주소 목록을 가져옵니다. (루프백 주소 제외)
    -   각 IP 주소에 대해 **TCP 80 포트**로 `socket.connect_ex`를 사용하여 연결을 시도하고 응답 시간을 측정합니다.
    -   3회 평균 응답 시간을 계산하여 신뢰도를 높입니다.
    -   결과를 CSV 파일로 저장하고, 가장 빠른 IP와 느린 IP 정보를 포함하여 반환합니다.

-   **코드 조각**
    ```python
    # (요약) TCP 80 포트로 소켓 연결을 시도하여 응답 시간 측정
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    start_time = time.perf_counter()
    # connect_ex는 non-blocking이며, 성공 시 0을 반환
    result_code = sock.connect_ex((ip, 80))
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    sock.close()
    ```

</details>

<details>
<summary><strong>3. OS별 DNS 적용/리셋 (services/dns_service.py)</strong></summary>

-   **핵심 로직**
    -   `platform.system()`으로 현재 운영체제(Windows, Darwin, Linux)를 식별합니다.
    -   **OS별 네이티브 명령어**를 동적으로 구성하여 실행합니다.
        -   **Windows**: `netsh interface ip set dns name="<어댑터>" static <IP>`
        -   **macOS**: `networksetup -setdnsservers "<서비스명>" <IP>`
        -   **Linux**: `echo "nameserver <IP>" | sudo tee /etc/resolv.conf`
    -   Windows와 macOS에서는 현재 활성화된 네트워크 어댑터/서비스 이름을 자동으로 탐지합니다.
    -   DNS 변경 시 권한 부족이 감지되면, **명령어 단위로 권한을 승격**하여 재시도하는 로직이 포함되어 있습니다. (Windows UAC 자동 처리)

-   **코드 조각**
    ```python
    # (요약) OS를 확인하고 그에 맞는 DNS 변경 명령어를 생성 및 실행
    system = platform.system()
    if system == "Windows":
        adapter = DNSService.detect_active_adapter_win()
        command = f'netsh interface ip set dns name="{adapter}" static {dns_ip}'
    elif system == "Darwin": # macOS
        service = DNSService.detect_active_adapter_mac()
        command = f'networksetup -setdnsservers "{service}" {dns_ip}'
    else: # Linux
        command = f'echo "nameserver {dns_ip}" | sudo tee /etc/resolv.conf > /dev/null'

    # 생성된 명령어를 subprocess로 실행
    # ...
    ```

</details>

## 🙌 기여하기

이 프로젝트에 기여하고 싶으시다면 언제든지 환영합니다!

1.  이 저장소를 **Fork**하세요.
2.  새로운 기능이나 버그 수정을 위한 브랜치를 만드세요. (`git checkout -b feature/amazing-feature`)
3.  코드를 수정하고 커밋하세요. (`git commit -m 'Add some amazing feature'`)
4.  Fork한 저장소에 Push하세요. (`git push origin feature/amazing-feature`)
5.  **Pull Request**를 열어주세요.

## 📄 라이선스

본 프로젝트는 **MIT License**를 따릅니다. 자세한 내용은 `LICENSE` 파일을 참고하세요.
