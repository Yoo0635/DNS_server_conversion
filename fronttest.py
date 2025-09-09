import sys, requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QLabel, QPushButton, QTextEdit, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import QThread, pyqtSignal

API_BASE = "http://127.0.0.1:8000"

class Worker(QThread):
    done = pyqtSignal(str)
    def __init__(self, domain: str, count: int):
        super().__init__()
        self.domain, self.count = domain, count
    def run(self):
        try:
            r = requests.get(
                f"{API_BASE}/measure",
                params={"domain": self.domain, "count": self.count},
                timeout=10
            )
            self.done.emit(r.text)
        except Exception as e:
            self.done.emit(f"error: {e}")

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("이 영광을 아이브에게 바칩니다.")

        self.domain = QLineEdit("ticket.melon.com")
        self.count = QLineEdit("5")
        self.btn = QPushButton("측정")
        self.out = QTextEdit(); self.out.setReadOnly(True)

        row = QHBoxLayout()
        row.addWidget(QLabel("도메인")); row.addWidget(self.domain)
        row.addWidget(QLabel("횟수")); row.addWidget(self.count)
        row.addWidget(self.btn)

        col = QVBoxLayout(self)
        col.addLayout(row)
        col.addWidget(self.out)

        self.btn.clicked.connect(self.run_measure)
        self.worker = None

    def run_measure(self):
        d = self.domain.text().strip()
        c = int(self.count.text().strip() or "1")
        self.btn.setEnabled(False)
        self.out.append(f"요청 → /measure?domain={d}&count={c}")
        self.worker = Worker(d, c)
        self.worker.done.connect(self.show_result)
        self.worker.start()

    def show_result(self, text: str):
        self.out.append(text)
        self.out.append("-" * 40)
        self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App(); w.resize(640, 420); w.show()
    sys.exit(app.exec_())
