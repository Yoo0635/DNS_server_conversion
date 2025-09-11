import requests
from PyQt5.QtWidgets import QMessageBox

def change_dns_server(new_dns_ip, parent_ui):
    """
    백엔드 API를 호출하여 DNS 서버를 변경하고 UI를 업데이트합니다.
    :param new_dns_ip: 변경할 DNS 서버 IP 주소
    :param parent_ui: 상태 라벨을 포함하는 부모 UI 객체 (DashboardUI)
    """
    url = "http://127.0.0.1:8000/change-dns"
    payload = {"new_dns": new_dns_ip}
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        response_data = response.json()
        
        # 성공 메시지를 UI에 표시
        parent_ui.status_label.setText(f"✅ DNS 서버가 {new_dns_ip}로 변경되었습니다.")
        QMessageBox.information(parent_ui, "성공", response_data.get("message", "DNS 서버 변경 완료"))
        
    except requests.exceptions.RequestException as e:
        # 오류 메시지를 UI에 표시
        parent_ui.status_label.setText(f"❌ 오류 발생: {e}")
        QMessageBox.critical(parent_ui, "오류", f"DNS 서버 변경 중 오류 발생: {e}")