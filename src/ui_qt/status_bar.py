import logging
from PySide6.QtWidgets import (
    QStatusBar,
    QLabel,
)

from PySide6.QtCore import Slot

from interfaces.qt.controller import QtController

logger = logging.getLogger(__name__)


class StatusBarWidget(QStatusBar):
    def __init__(self, qt_controller: QtController):
        super().__init__()

        self.labels = {}
        self.qt_controller = qt_controller
        self.qt_controller.status_bar_updated.connect(self.update_label)

        self.setup_ui()

    def setup_ui(self):
        self.transport_label = QLabel("连接：未打开  ")
        self.addWidget(self.transport_label)
        self.labels["transport"] = self.transport_label

        self.light_label = QLabel("光源：未打开  ")
        self.addWidget(self.light_label)
        self.labels["light"] = self.light_label

        self.laser_label = QLabel("激光：未打开  ")
        self.addWidget(self.laser_label)
        self.labels["laser"] = self.laser_label

        self.temperature_label = QLabel("温度：--  ")
        self.addWidget(self.temperature_label)
        self.labels["temperature"] = self.temperature_label

        self.humidity_label = QLabel("湿度：--  ")
        self.addWidget(self.humidity_label)
        self.labels["humidity"] = self.humidity_label

    @Slot(str, object)
    def update_label(self, key: str, value: object):
        if key in self.labels:
            label = self.labels[key]

            if key == "transport":
                label.setText(f"连接：{value}  ")
            elif key == "light":
                label.setText(f"光源：{value}  ")
            elif key == "laser":
                label.setText(f"激光：{value}  ")
            elif key == "temperature":
                label.setText(f"温度：{value}  ")
            elif key == "humidity":
                label.setText(f"湿度：{value}  ")
            else:
                logger.warning(f"未知的状态键：{key}")
