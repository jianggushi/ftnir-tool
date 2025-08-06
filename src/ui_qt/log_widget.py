import logging
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPlainTextEdit,
)
from PySide6.QtCore import Slot, QObject, Signal, Qt


logger = logging.getLogger(__name__)


class LogHandler(logging.Handler, QObject):
    log_signal = Signal(str)

    def __init__(self):
        # 显示初始化两个父类
        logging.Handler.__init__(self)
        QObject.__init__(self)

    def emit(self, record):
        msg = self.format(record)
        self.log_signal.emit(msg)


class LogWidget(QDialog):
    def __init__(self):
        super().__init__()

        self.log_handler = LogHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s"
        )
        self.log_handler.setFormatter(formatter)

        self.log_handler.log_signal.connect(self.append_log, Qt.QueuedConnection)
        # 将 handler 添加到 root logger 以捕获所有日志
        logging.getLogger().addHandler(self.log_handler)

        self.setWindowTitle("日志")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.log_view = QPlainTextEdit()
        self.log_view.setReadOnly(True)
        main_layout.addWidget(self.log_view)

    @Slot(str)
    def append_log(self, msg):
        self.log_view.appendPlainText(msg)
