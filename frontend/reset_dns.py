import requests
from PyQt5.QtWidgets import QMessageBox

def reset_dns_server(parent_ui):
    """
    백엔드 API를 호출하여 DNS 서버를 기본값으로 초기화하고 UI를 업데이트합니다.
    :param parent_ui: 상태 라벨을 포함하는 부모 UI 객체 (DashboardUI)
    """
    url = "http://127.0.0.1:8000/reset-dns"
    
    try:
        response = requests.post(url)
        response.raise_for_status()
        response_data = response.json()
        
        # 성공 메시지를 UI에 표시
        parent_ui.status_label.setText("✅ DNS 서버가 기본값으로 초기화되었습니다.")
        QMessageBox.information(parent_ui, "성공", response_data.get("message", "DNS 서버 초기화 완료"))
        
    except requests.exceptions.RequestException as e:
        # 오류 메시지를 UI에 표시
        parent_ui.status_label.setText(f"❌ 오류 발생: {e}")
        QMessageBox.critical(parent_ui, "오류", f"DNS 서버 초기화 중 오류 발생: {e}")