"""
Network Performance Optimizer - PyQt5 Frontend
메인 애플리케이션 진입점
"""

import sys
from PyQt5.QtWidgets import QApplication
from pyqt_window import MainWindow


def main():
    """메인 애플리케이션 실행"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
