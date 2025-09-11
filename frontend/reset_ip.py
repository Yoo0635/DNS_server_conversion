from PyQt5.QtWidgets import QMessageBox

def reset_ip_address(parent_ui):
    """
    IP 설정을 초기화하는 기능을 수행하고 UI를 업데이트합니다.
    (백엔드에 관련 API가 구현되어야 함)
    :param parent_ui: 상태 라벨을 포함하는 부모 UI 객체 (DashboardUI)
    """
    # 이 부분은 백엔드에 해당하는 API를 만들어야 합니다.
    # 예: url = "http://127.0.0.1:8000/reset-ip"
    
    # 현재는 가상 로직으로 동작을 시뮬레이션
    try:
        parent_ui.status_label.setText("✅ IP 설정이 초기화되었습니다.")
        QMessageBox.information(parent_ui, "성공", "IP 설정이 초기화되었습니다.")

    except Exception as e:
        parent_ui.status_label.setText(f"❌ 오류 발생: {e}")
        QMessageBox.critical(parent_ui, "오류", f"IP 초기화 중 오류 발생: {e}")