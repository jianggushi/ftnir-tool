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

from .control_collect import CollectWidget
from .control_hardware import HardwareSettingWidget


class CommunicationWidget(QGroupBox):
    def __init__(self):
        super().__init__("通信设置")

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # port layout
        self.port_combo = QComboBox()
        self.refresh_button = QPushButton("刷新")
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("端口："))
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_button)

        main_layout.addLayout(port_layout)

        # button layout
        self.connect_btn = QPushButton("连接")
        self.disconnect_btn = QPushButton("断开")
        self.disconnect_btn.setEnabled(False)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.disconnect_btn)

        main_layout.addLayout(button_layout)

    def get_port(self) -> str:
        return self.port_combo.currentText()

    def set_connect(self):
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)

    def set_disconnect(self):
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)

    def refresh_ports(self, ports: list[str]):
        self.port_combo.clear()
        self.port_combo.addItems(ports)


class LightWidget(QGroupBox):
    def __init__(self):
        super().__init__("光源/激光控制")

        self.light_on = False
        self.laser_on = False

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        light_layout = QHBoxLayout()
        self.light_button = QPushButton(self.light_text)
        light_layout.addWidget(self.light_button)
        self.laser_button = QPushButton(self.laser_text)
        light_layout.addWidget(self.laser_button)

        main_layout.addLayout(light_layout)

    @property
    def light_text(self) -> str:
        if self.light_on:
            return "关闭光源"
        else:
            return "打开光源"

    @property
    def laser_text(self) -> str:
        if self.laser_on:
            return "关闭激光"
        else:
            return "打开激光"

    def turn_on_light(self):
        self.light_on = True
        self.light_button.setText(self.light_text)

    def turn_off_light(self):
        self.light_on = False
        self.light_button.setText(self.light_text)

    def turn_on_laser(self):
        self.laser_on = True
        self.laser_button.setText(self.laser_text)

    def turn_off_laser(self):
        self.laser_on = False
        self.laser_button.setText(self.laser_text)


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


class ControlWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.comm_widget = CommunicationWidget()
        main_layout.addWidget(self.comm_widget)

        self.light_widget = LightWidget()
        main_layout.addWidget(self.light_widget)

        self.rotate_widget = RotateMotorWidget()
        main_layout.addWidget(self.rotate_widget)

        self.screw_widget = ScrewMotorWidget()
        main_layout.addWidget(self.screw_widget)

        self.hardware_widget = HardwareSettingWidget()
        main_layout.addWidget(self.hardware_widget)

        self.collect_widget = CollectWidget()
        main_layout.addWidget(self.collect_widget)

        main_layout.addStretch()
