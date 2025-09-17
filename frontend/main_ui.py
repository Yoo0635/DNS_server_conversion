# frontend/main_ui.py

import tkinter as tk
import platform
import sys
import os
from .dashboard_ui import DashboardUI

class NetworkOptimizerApp:
    """네트워크 성능 최적화 메인 애플리케이션"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_ui()
        
    def setup_window(self):
        """윈도우 설정"""
        # 크로스 플랫폼 윈도우 설정
        self.root.title("🌐 Network Performance Optimizer")
        
        # 플랫폼별 최적 크기 설정
        if platform.system() == "Darwin":  # macOS
            self.root.geometry("1200x800")
            # macOS 네이티브 스타일
            try:
                self.root.configure(bg='#f5f5f7')
            except:
                pass
        elif platform.system() == "Windows":
            self.root.geometry("1200x800")
            self.root.configure(bg='#f8f9fa')
        else:  # Linux
            self.root.geometry("1200x800")
            self.root.configure(bg='#ffffff')
        
        # 최소 크기 설정
        self.root.minsize(800, 600)
        
        # 아이콘 설정 (있는 경우)
        try:
            if platform.system() == "Windows":
                self.root.iconbitmap("icon.ico")
            else:
                self.root.iconphoto(True, tk.PhotoImage(file="icon.png"))
        except:
            pass
        
        # 윈도우 중앙 배치
        self.center_window()
        
        # 종료 이벤트 처리
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def setup_ui(self):
        """UI 설정"""
        try:
            self.dashboard = DashboardUI(master=self.root)
        except Exception as e:
            # 오류 발생 시 기본 UI 표시
            error_label = tk.Label(
                self.root,
                text=f"UI 로딩 오류: {str(e)}\n\n프로그램을 다시 시작해주세요.",
                font=('Arial', 12),
                fg='red',
                justify='center'
            )
            error_label.pack(expand=True)
            
    def on_closing(self):
        """애플리케이션 종료 처리"""
        try:
            # 정리 작업
            if hasattr(self, 'dashboard'):
                self.dashboard.destroy()
            self.root.destroy()
        except:
            self.root.destroy()
            
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            print(f"애플리케이션 실행 중 오류: {e}")
            self.on_closing()

def main():
    """메인 함수"""
    try:
        app = NetworkOptimizerApp()
        app.run()
    except Exception as e:
        print(f"애플리케이션 시작 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()