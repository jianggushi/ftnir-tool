import sys
import logging
from PySide6.QtWidgets import QApplication

from config.log import setup_logging
from gui.main_window import MainWindow


logger = logging.getLogger(__name__)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("光谱上位机系统")
    app.setApplicationVersion("1.0.0")

    main_window = MainWindow()
    main_window.show()

    app.exit(app.exec())


if __name__ == "__main__":
    setup_logging()
    main()
