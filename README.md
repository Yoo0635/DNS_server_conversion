# Network Performance Optimizer v1.0.1

🚀 **Windows 지원 완료!** 크로스 플랫폼 DNS 성능 최적화 도구

## ✨ 주요 기능
- 🌐 DNS 서버 성능 측정 및 비교
- 📊 실시간 차트 시각화
- 🔧 원클릭 DNS 서버 변경
- 🖥️ Windows/macOS/Linux 지원
- 🔐 Windows UAC 자동 처리

## 🌐 지원 DNS 서버
- Google (8.8.8.8)
- KT (168.126.63.1)
- SKB (219.250.36.130)
- LGU+ (164.124.101.2)
- KISA (203.248.252.2)

## 🚀 빠른 시작

### Windows (권장)
1. `NetworkOptimizer-Windows.exe` 다운로드
2. 더블클릭 실행
3. UAC 팝업에서 '예' 클릭
4. DNS 서버 선택 후 'Apply DNS' 클릭

### 소스 실행
```bash
pip install -r requirements.txt
python run_app.py
```

## 💻 시스템 요구사항
- Windows 10/11 (권장)
- macOS 10.15+
- Linux (Ubuntu 18.04+)
- Python 3.8+ (소스 실행 시)

## 🛠️ 기술 스택
- **Backend**: FastAPI + Uvicorn
- **Frontend**: PyQt5 + Matplotlib
- **DNS**: dnspython
- **Build**: PyInstaller

## 📄 라이선스
MIT License

## 🤝 기여하기
버그 리포트나 기능 제안은 Issues에서 해주세요!

---
**v1.0.1** - Windows UAC 지원, AdminChecker 제거, 성능 최적화