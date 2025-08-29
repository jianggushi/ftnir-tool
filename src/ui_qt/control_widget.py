from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
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
from .control_motor import RotateMotorWidget, ScrewMotorWidget


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


class PwmWidget(QGroupBox):
    def __init__(self):
        super().__init__("PWM控制")
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        form_layout = QFormLayout()
        main_layout.addLayout(form_layout)

        # 周期
        self.period_input = QLineEdit()
        self.period_input.setText("20")
        form_layout.addRow(QLabel("周期(ns):"), self.period_input)
        # 占空比
        self.duty_spinbox = QSpinBox(minimum=0, maximum=100, singleStep=1)
        self.duty_spinbox.setValue(10)
        form_layout.addRow(QLabel("占空比(%):"), self.duty_spinbox)

        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        button_layout.addStretch()
        self.set_button = QPushButton("设置")
        button_layout.addWidget(self.set_button)

    def get_pwm_param(self) -> tuple[int, int]:
        period = int(self.period_input.text())
        duty = self.duty_spinbox.value()
        return period, duty


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

        self.pwm_widget = PwmWidget()
        main_layout.addWidget(self.pwm_widget)

        self.hardware_widget = HardwareSettingWidget()
        main_layout.addWidget(self.hardware_widget)

        self.collect_widget = CollectWidget()
        main_layout.addWidget(self.collect_widget)

        main_layout.addStretch()
