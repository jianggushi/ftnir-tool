from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QPushButton,
    QComboBox,
    QLabel,
    QFormLayout,
    QSpinBox,
)
from PySide6.QtCore import Slot


class RotateMotorWidget(QGroupBox):
    def __init__(self):
        super().__init__("旋转电机")

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        offset_layout = QHBoxLayout()
        self.offset_spinbox = QSpinBox(minimum=0, singleStep=1)
        self.offset_button = QPushButton("设置偏移")
        offset_layout.addWidget(QLabel("偏移(步数):"))
        offset_layout.addWidget(self.offset_spinbox)
        offset_layout.addWidget(self.offset_button)

        main_layout.addLayout(offset_layout)
        main_layout.addWidget(QLabel("目标:"))

        target_layout = QGridLayout()
        self.target_1_button = QPushButton("1")
        self.target_2_button = QPushButton("2")
        self.target_3_button = QPushButton("3")
        self.target_4_button = QPushButton("4")
        self.target_5_button = QPushButton("5")
        self.target_6_button = QPushButton("6")
        self.target_reset_button = QPushButton("复位")
        target_layout.addWidget(self.target_1_button, 0, 0)
        target_layout.addWidget(self.target_2_button, 0, 1)
        target_layout.addWidget(self.target_3_button, 0, 2)
        target_layout.addWidget(self.target_4_button, 0, 3)
        target_layout.addWidget(self.target_5_button, 1, 0)
        target_layout.addWidget(self.target_6_button, 1, 1)
        target_layout.addWidget(self.target_reset_button, 1, 2)

        main_layout.addLayout(target_layout)

    def get_offset(self) -> int:
        offset = self.offset_spinbox.value()
        return offset


class ScrewMotorWidget(QGroupBox):
    def __init__(self):
        super().__init__("丝杆电机")

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        offset_layout = QHBoxLayout()
        self.offset_spinbox = QSpinBox(minimum=0, singleStep=1)
        self.offset_button = QPushButton("设置偏移")
        offset_layout.addWidget(QLabel("偏移(距离mm):"))
        offset_layout.addWidget(self.offset_spinbox)
        offset_layout.addWidget(self.offset_button)

        main_layout.addLayout(offset_layout)
        main_layout.addWidget(QLabel("目标:"))

        target_layout = QGridLayout()
        self.target_1_button = QPushButton("1")
        self.target_2_button = QPushButton("2")
        self.target_3_button = QPushButton("3")
        self.target_4_button = QPushButton("4")
        self.target_5_button = QPushButton("5")
        self.target_6_button = QPushButton("6")
        self.target_7_button = QPushButton("7")
        self.target_8_button = QPushButton("8")
        self.target_reset_button = QPushButton("复位")
        self.target_hide_button = QPushButton("遮挡")
        target_layout.addWidget(self.target_1_button, 0, 0)
        target_layout.addWidget(self.target_2_button, 0, 1)
        target_layout.addWidget(self.target_3_button, 0, 2)
        target_layout.addWidget(self.target_4_button, 0, 3)
        target_layout.addWidget(self.target_5_button, 1, 0)
        target_layout.addWidget(self.target_6_button, 1, 1)
        target_layout.addWidget(self.target_7_button, 1, 2)
        target_layout.addWidget(self.target_8_button, 1, 3)
        target_layout.addWidget(self.target_reset_button, 2, 0)
        target_layout.addWidget(self.target_hide_button, 2, 1)

        main_layout.addLayout(target_layout)

    def get_offset(self) -> int:
        offset = self.offset_spinbox.value()
        return offset
