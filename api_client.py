# api_client.py
import requests
import time
import random

# --- 실제 백엔드 API 주소 (나중에 백엔드 팀과 협의하여 변경) ---
BASE_API_URL = "http://localhost:8000/api" # 예시 URL

def request_reservation(user_id: str, ticket_count: int):
    """
    백엔드 서버에 티켓 예매를 요청하고 응답을 받습니다.
    (현재는 가상 응답을 반환하여 UI 테스트용)
    """
    print(f"DEBUG: 백엔드에 예매 요청 시뮬레이션 - 유저: {user_id}, 티켓 수: {ticket_count}")

    # --- 실제 API 호출 (나중에 이 부분을 활성화) ---
    # try:
    #     response = requests.post(f"{BASE_API_URL}/reserve", json={
    #         "user_id": user_id,
    #         "ticket_count": ticket_count
    #     })
    #     response.raise_for_status() # HTTP 오류가 발생하면 예외 발생
    #     return response.json()
    # except requests.exceptions.RequestException as e:
    #     print(f"API 요청 오류: {e}")
    #     return {"status": "error", "message": "네트워크 오류 발생."}

    # --- 가상(Dummy) 응답 시뮬레이션 (현재 활성화) ---
    # 실제 백엔드 서버가 없을 때 UI 테스트용으로 사용
    time.sleep(2) # API 호출에 2초 걸린다고 가정

    # 무작위로 성공, 실패, 대기열 응답 반환
    scenario = random.choices(["success", "fail", "queue"], weights=[0.6, 0.2, 0.2], k=1)[0]

    if scenario == "success":
        return {"status": "success", "message": "예매 성공! 티켓이 발급되었습니다."}
    elif scenario == "queue":
        return {"status": "queue", "message": "현재 대기열에 진입했습니다.", "queue_position": random.randint(1, 100)}
    else: # fail
        return {"status": "error", "message": "죄송합니다. 티켓 예매에 실패했습니다. 재시도 해주세요."}

# 다른 API 함수들 (예: 좌석 조회, 대기열 상태 조회 등)도 여기에 정의
def get_available_seats():
    print("DEBUG: 백엔드에 좌석 조회 요청 시뮬레이션")
    time.sleep(1)
    return {"status": "success", "available_seats": random.randint(50, 200)}

def get_queue_status():
    print("DEBUG: 백엔드에 대기열 상태 조회 요청 시뮬레이션")
    time.sleep(1)
    return {"status": "success", "current_queue": random.randint(0, 50)}