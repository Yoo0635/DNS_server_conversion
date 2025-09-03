# frontend/reset_dns.py

import requests
import threading
import tkinter as tk

def reset_dns(app_instance):
    app_instance.dns_result_text.delete(1.0, tk.END)
    app_instance.dns_result_text.insert(tk.END, "DNS 서버를 초기화 중...\n")
    app_instance.reset_dns_button.config(state=tk.DISABLED)

    def run_reset_request():
        try:
            # 백엔드 API에 POST 요청 보내기
            response = requests.post("http://127.0.0.1:8000/reset-dns")
            
            if response.status_code == 200:
                result_data = response.json()
                if result_data.get("status") == "success":
                    app_instance.queue.put(("update_dns_change", "✅ DNS 서버가 기본값으로 초기화되었습니다."))
                else:
                    app_instance.queue.put(("error", f"오류: {result_data.get('message')}"))
            else:
                app_instance.queue.put(("error", f"백엔드 서버 오류: {response.status_code}"))
        except requests.exceptions.ConnectionError:
            app_instance.queue.put(("error", "오류: 백엔드 서버가 실행 중이지 않습니다."))
        except Exception as e:
            app_instance.queue.put(("error", f"알 수 없는 오류 발생: {e}"))

    threading.Thread(target=run_reset_request).start()