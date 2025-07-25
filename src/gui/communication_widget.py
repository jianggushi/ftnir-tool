from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
)
from PySide6.QtCore import Slot, Signal


class CommunicationWidget(QGroupBox):
    # 定义信号
    connected = Signal()
    disconnected = Signal()

    def __init__(self, parent=None):
        super().__init__("通信设置", parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        comm_layout = QVBoxLayout()
        self.setLayout(comm_layout)

        # Buttons layout
        button_layout = QHBoxLayout()

        # Connect button
        self.connect_btn = QPushButton("连接")
        self.connect_btn.clicked.connect(self.on_connect)

        # Disconnect button
        self.disconnect_btn = QPushButton("断开")
        self.disconnect_btn.clicked.connect(self.on_disconnect)
        self.disconnect_btn.setEnabled(False)

        # Add buttons to layout
        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.disconnect_btn)

        # Add button layout to main layout
        comm_layout.addLayout(button_layout)

    @Slot()
    def on_connect(self):
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)
        self.connected.emit()

    @Slot()
    def on_disconnect(self):
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.disconnected.emit()
