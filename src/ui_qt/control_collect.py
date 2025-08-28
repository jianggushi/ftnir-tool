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

from config.types import SpectrumData


class CollectWidget(QGroupBox):

    def __init__(self):
        super().__init__("数据采集")

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

        show_layout = QHBoxLayout()
        show_layout.addWidget(QLabel("显示:"))
        self.show_ax_checkbox = QCheckBox("干涉图")
        self.show_bx_checkbox = QCheckBox("光谱图")
        self.show_ax_checkbox.setChecked(True)
        self.show_bx_checkbox.setChecked(True)
        show_layout.addWidget(self.show_ax_checkbox)
        show_layout.addWidget(self.show_bx_checkbox)
        main_layout.addLayout(show_layout)

    def setup_signals(self):
        self.continuous_mode.toggled.connect(self.on_continuous_toggled)

    @Slot()
    def on_continuous_toggled(self):
        self.num_input.setEnabled(not self.continuous_mode.isChecked())

    def get_continuous_mode(self) -> bool:
        return self.continuous_mode.isChecked()

    def get_collect_num(self) -> int:
        num = int(self.num_input.text())
        if self.continuous_mode.isChecked():
            num = 0
        return num

    def start_collect(self):
        """开始采集"""
        self.target_num = self.get_collect_num()

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_collect(self):
        """停止采集"""
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def on_receive_data(self, data: SpectrumData):
        """处理暗噪声数据"""
        if self.target_num > 0:
            self.target_num -= 1
            if self.target_num == 0:
                self.stop_collect()
