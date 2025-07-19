import sys
from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("光谱上位机系统")
    app.setApplicationVersion("1.0.0")

    main_window = MainWindow()
    main_window.show()

    app.exit(app.exec())


if __name__ == "__main__":
    main()
