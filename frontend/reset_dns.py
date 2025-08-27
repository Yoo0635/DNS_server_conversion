# frontend/reset_dns.py

import requests
import threading
import queue
import tkinter as tk

def reset_dns(app_instance):
    app_instance.dns_result_text.insert(tk.END, "DNS 초기화 기능은 아직 구현되지 않았습니다.\n")
    # 여기에 나중에 DNS 초기화 로직을 추가할 겁니다.