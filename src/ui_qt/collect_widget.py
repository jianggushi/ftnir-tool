import numpy as np
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QButtonGroup,
    QPushButton,
    QGroupBox,
    QLabel,
    QRadioButton,
    QLineEdit,
    QCheckBox,
)
from PySide6.QtCore import Signal, Slot

from core.model.spectrum import SpectrumData
from interfaces.qt.controller import QtController


class CollectWidget(QGroupBox):

    def __init__(self, qt_controller: QtController = None):
        super().__init__("数据采集")

        self.controller = qt_controller
        # self.controller.dark_noise_handler.add_callback(self.on_dark_noise_received)
        # self.controller.background_handler.add_callback(self.on_dark_noise_received)
        # self.controller.sample_handler.add_callback(self.on_dark_noise_received)

        self.target_num = 0

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("类型:"))
        self.dark_noise_radio = QRadioButton("暗噪声")
        self.background_radio = QRadioButton("背景")
        self.sample_radio = QRadioButton("样品")
        self.sample_radio.setChecked(True)
        type_group = QButtonGroup(self)
        type_group.addButton(self.dark_noise_radio)
        type_group.addButton(self.background_radio)
        type_group.addButton(self.sample_radio)
        type_layout.addWidget(self.dark_noise_radio)
        type_layout.addWidget(self.background_radio)
        type_layout.addWidget(self.sample_radio)

        main_layout.addLayout(type_layout)

        num_layout = QHBoxLayout()
        num_layout.addWidget(QLabel("次数:"))
        self.num_input = QLineEdit()
        self.num_input.setText("1")
        num_layout.addWidget(self.num_input)
        self.continuous_mode = QCheckBox("连续")
        num_layout.addWidget(self.continuous_mode)

        main_layout.addLayout(num_layout)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始采集")
        self.stop_button = QPushButton("停止采集")
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        main_layout.addLayout(button_layout)

    def setup_signals(self):
        self.continuous_mode.toggled.connect(self.on_continuous_toggled)

        self.start_button.clicked.connect(self.start_collect)
        self.stop_button.clicked.connect(self.stop_collect)

    @Slot()
    def on_continuous_toggled(self):
        self.num_input.setEnabled(not self.continuous_mode.isChecked())

    @Slot()
    def start_collect(self):
        """开始采集"""
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        continuous_mode = self.continuous_mode.isChecked()
        num = int(self.num_input.text())
        if continuous_mode:
            num = 0

        self.target_num = num

        if self.dark_noise_radio.isChecked():
            self.controller.collect_dark_noise(num, continuous_mode)
        elif self.background_radio.isChecked():
            self.controller.collect_background(num, continuous_mode)
        elif self.sample_radio.isChecked():
            self.controller.collect_sample(num, continuous_mode)

    @Slot()
    def stop_collect(self):
        """停止采集"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.controller.collect_stop()

    def on_dark_noise_received(self, spectrum_data: SpectrumData):
        """处理暗噪声数据"""
        if self.target_num > 0:
            self.target_num -= 1
            if self.target_num == 0:
                self.stop_collect()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = CollectWidget()
    widget.show()
    sys.exit(app.exec())
