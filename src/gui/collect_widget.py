import numpy as np
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGroupBox,
)
from PySide6.QtCore import Signal, Slot, QTimer


class CollectWidget(QGroupBox):
    # 信号，用于通知采集数据
    data_collected = Signal(list, list)

    def __init__(self):
        super().__init__("数据采集")
        self.setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.collect_data)

        # 状态变量
        self.is_continuous = False
        self.collect_count = 0
        self.target_count = 0

    def setup_ui(self):
        """设置UI布局"""
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 开始采集按钮
        self.start_button = QPushButton("开始采集")
        self.start_button.clicked.connect(self.start_collect)

        # 停止采集按钮
        self.stop_button = QPushButton("停止采集")
        self.stop_button.clicked.connect(self.stop_collect)
        self.stop_button.setEnabled(False)

        # 添加按钮到布局
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        # 添加按钮布局到主布局
        layout.addLayout(button_layout)

    @Slot()
    def start_collect(self):
        """开始采集"""
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.timer.start(100)  # 每100ms采集一次数据

    @Slot()
    def stop_collect(self):
        """停止采集"""
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def collect_data(self):
        """采集数据"""
        # 模拟数据采集
        x_data = np.linspace(400, 4000, 1000).tolist()
        y_data = (
            np.sin(np.array(x_data) / 100) + np.random.random(1000) * 0.1
        ).tolist()

        # 发送采集数据信号
        self.data_collected.emit(x_data, y_data)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = CollectWidget()
    widget.show()
    sys.exit(app.exec())
