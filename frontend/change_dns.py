# frontend/change_dns.py

import requests
import threading
import tkinter as tk

# 백엔드 dns_servers.py 파일에 있는 딕셔너리를 복사해서 사용합니다.
# 이렇게 해야 상대 경로(.) 오류 없이 동작합니다.
dns_servers = {
    "Google": "8.8.8.8",
    "KT": "168.126.63.1",
    "SKB": "219.250.36.130",
    "LGU+": "164.124.101.2",
    "KISA": "203.248.252.2"
}

def change_dns(app_instance):
    # ticket_ui.py에서 저장한 IP 주소 변수를 사용
    new_dns_ip = app_instance.selected_dns_ip
    
    # 선택된 IP가 없을 경우 오류 처리
    if not new_dns_ip:
        app_instance.dns_result_text.delete(1.0, tk.END)
        app_instance.dns_result_text.insert(tk.END, "오류: 변경할 DNS 서버를 선택하세요.\n")
        return

    # IP 주소에 해당하는 이름 찾기
    new_dns_name = new_dns_ip
    for name, ip in dns_servers.items():
        if ip == new_dns_ip:
            new_dns_name = name
            break

    # 사용자에게 보여줄 메시지에 이름과 IP를 모두 포함
    message = f"DNS 서버를 {new_dns_name}({new_dns_ip})로 변경 중...\n"
    app_instance.dns_result_text.delete(1.0, tk.END)
    app_instance.dns_result_text.insert(tk.END, message)
    app_instance.change_dns_button.config(state=tk.DISABLED)

    def run_change_request():
        try:
            # 백엔드 API에 POST 요청 보내기
            response = requests.post("http://127.0.0.1:8000/change-dns", json={"new_dns": new_dns_ip})
            
            if response.status_code == 200:
                result_data = response.json()
                if result_data.get("status") == "success":
                    app_instance.queue.put(("update_dns_change", f"✅ DNS 서버 변경 성공: {new_dns_name}({new_dns_ip})"))
                else:
                    app_instance.queue.put(("error", f"오류: {result_data.get('message')}"))
            else:
                app_instance.queue.put(("error", f"백엔드 서버 오류: {response.status_code}"))
        except requests.exceptions.ConnectionError:
            app_instance.queue.put(("error", "오류: 백엔드 서버가 실행 중이지 않습니다."))
        except Exception as e:
            app_instance.queue.put(("error", f"알 수 없는 오류 발생: {e}"))

    threading.Thread(target=run_change_request).start()