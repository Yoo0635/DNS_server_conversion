import requests
from PyQt5.QtWidgets import QMessageBox

def fix_ip_address(fastest_ip, parent_ui):
    """
    가장 빠른 IP로 접속을 고정하는 기능을 수행하고 UI를 업데이트합니다.
    (백엔드에 관련 API가 구현되어야 함)
    :param fastest_ip: 고정할 IP 주소
    :param parent_ui: 상태 라벨을 포함하는 부모 UI 객체 (DashboardUI)
    """
    # 이 부분은 백엔드에 해당하는 API를 만들어야 합니다.
    # 예: url = "http://127.0.0.1:8000/fix-ip"
    # 예: payload = {"ip": fastest_ip}
    
    # 현재는 가상 로직으로 동작을 시뮬레이션
    try:
        parent_ui.status_label.setText(f"✅ IP 주소가 {fastest_ip}로 고정되었습니다.")
        QMessageBox.information(parent_ui, "성공", f"IP 주소가 {fastest_ip}로 고정되었습니다.")

    except Exception as e:
        parent_ui.status_label.setText(f"❌ 오류 발생: {e}")
        QMessageBox.critical(parent_ui, "오류", f"IP 고정 중 오류 발생: {e}")