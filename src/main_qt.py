import sys
import os
import logging
from PySide6.QtWidgets import QApplication

from config.log import setup_logging
from ui_qt.main_window import MainWindow
from interfaces.qt.main import MainController


logger = logging.getLogger(__name__)

os.environ["QT_API"] = "PySide6"


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("光谱上位机系统")
    app.setApplicationVersion("1.0.0")

    main_window = MainWindow()
    main_controller = MainController(main_window)

    main_window.show()

    app.exit(app.exec())


if __name__ == "__main__":
    setup_logging()
    main()
