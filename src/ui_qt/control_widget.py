from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGroupBox,
    QPushButton,
    QComboBox,
    QLabel,
    QLineEdit,
    QFrame,
    QFormLayout,
    QSpinBox,
    QDoubleSpinBox,
)
from PySide6.QtCore import Slot

from interfaces.qt.controller import QtController
from .collect_widget import CollectWidget


class CommunicationWidget(QGroupBox):

    def __init__(self, qt_controller: QtController):
        super().__init__("通信设置")

        self.qt_controller = qt_controller

        self.setup_ui()
        self.setup_signals()

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
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.connect_btn)
        button_layout.addWidget(self.disconnect_btn)

        main_layout.addLayout(button_layout)

    def setup_signals(self):
        self.connect_btn.clicked.connect(self.on_connect)
        self.disconnect_btn.clicked.connect(self.on_disconnect)
        self.disconnect_btn.setEnabled(False)
        self.refresh_button.clicked.connect(self.refresh_ports)

    @Slot()
    def on_connect(self):
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)
        port = self.port_combo.currentText()
        self.qt_controller.connect(port=port)

    @Slot()
    def on_disconnect(self):
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.qt_controller.disconnect()

    @Slot()
    def refresh_ports(self):
        self.port_combo.clear()
        ports = self.qt_controller.list_ports()
        self.port_combo.addItems(ports)


class LightWidget(QGroupBox):
    def __init__(self, qt_controller: QtController):
        super().__init__("光源/激光控制")

        self.qt_controller = qt_controller
        self.light_on = False
        self.laser_on = False

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        light_layout = QHBoxLayout()
        self.light_button = QPushButton(self.light_text)
        light_layout.addWidget(self.light_button)
        self.laser_button = QPushButton(self.laser_text)
        light_layout.addWidget(self.laser_button)

        main_layout.addLayout(light_layout)

    def setup_signals(self):
        self.light_button.clicked.connect(self.on_light_toggle)
        self.laser_button.clicked.connect(self.on_laser_toggle)

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
        self.qt_controller.turn_on_light()

    def turn_off_light(self):
        self.light_on = False
        self.light_button.setText(self.light_text)
        self.qt_controller.turn_off_light()

    @Slot()
    def on_light_toggle(self):
        if self.light_on:
            self.turn_off_light()
        else:
            self.turn_on_light()

    def turn_on_laser(self):
        self.laser_on = True
        self.laser_button.setText(self.laser_text)
        self.qt_controller.turn_on_laser()

    def turn_off_laser(self):
        self.laser_on = False
        self.laser_button.setText(self.laser_text)
        self.qt_controller.turn_off_laser()

    @Slot()
    def on_laser_toggle(self):
        if self.laser_on:
            self.turn_off_laser()
        else:
            self.turn_on_laser()


class RotateMotorWidget(QGroupBox):
    def __init__(self, qt_controller: QtController):
        super().__init__("旋转电机")

        self.qt_controller = qt_controller

        self.setup_ui()
        self.setup_signals()

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

    def setup_signals(self):
        self.offset_button.clicked.connect(self.on_offset_set)
        self.target_1_button.clicked.connect(self.on_target_1_set)
        self.target_2_button.clicked.connect(self.on_target_2_set)
        self.target_3_button.clicked.connect(self.on_target_3_set)
        self.target_4_button.clicked.connect(self.on_target_4_set)
        self.target_5_button.clicked.connect(self.on_target_5_set)
        self.target_6_button.clicked.connect(self.on_target_6_set)
        self.target_reset_button.clicked.connect(self.on_target_reset_set)

    @Slot()
    def on_offset_set(self):
        offset = self.offset_spinbox.value()
        self.qt_controller.set_rotate_offset(offset)

    @Slot()
    def on_target_1_set(self):
        self.qt_controller.set_rotate_target(1)

    @Slot()
    def on_target_2_set(self):
        self.qt_controller.set_rotate_target(2)

    @Slot()
    def on_target_3_set(self):
        self.qt_controller.set_rotate_target(3)

    @Slot()
    def on_target_4_set(self):
        self.qt_controller.set_rotate_target(4)

    @Slot()
    def on_target_5_set(self):
        self.qt_controller.set_rotate_target(5)

    @Slot()
    def on_target_6_set(self):
        self.qt_controller.set_rotate_target(6)

    @Slot()
    def on_target_reset_set(self):
        self.qt_controller.set_rotate_target(0)


class ScrewMotorWidget(QGroupBox):
    def __init__(self, qt_controller: QtController):
        super().__init__("丝杆电机")

        self.qt_controller = qt_controller

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        offset_layout = QHBoxLayout()
        self.offset_spinbox = QDoubleSpinBox(minimum=0.00, singleStep=0.01)
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
        target_layout.addWidget(self.target_1_button, 0, 0)
        target_layout.addWidget(self.target_2_button, 0, 1)
        target_layout.addWidget(self.target_3_button, 0, 2)
        target_layout.addWidget(self.target_4_button, 0, 3)
        target_layout.addWidget(self.target_5_button, 1, 0)
        target_layout.addWidget(self.target_6_button, 1, 1)
        target_layout.addWidget(self.target_7_button, 1, 2)
        target_layout.addWidget(self.target_8_button, 1, 3)
        target_layout.addWidget(self.target_reset_button, 2, 0)

        main_layout.addLayout(target_layout)

    def setup_signals(self):
        self.offset_button.clicked.connect(self.on_offset_set)
        self.target_1_button.clicked.connect(self.on_target_1_set)
        self.target_2_button.clicked.connect(self.on_target_2_set)
        self.target_3_button.clicked.connect(self.on_target_3_set)
        self.target_4_button.clicked.connect(self.on_target_4_set)
        self.target_5_button.clicked.connect(self.on_target_5_set)
        self.target_6_button.clicked.connect(self.on_target_6_set)
        self.target_7_button.clicked.connect(self.on_target_7_set)
        self.target_8_button.clicked.connect(self.on_target_8_set)
        self.target_reset_button.clicked.connect(self.on_target_reset_set)

    @Slot()
    def on_offset_set(self):
        offset = self.offset_spinbox.value()
        self.qt_controller.set_screw_offset(offset)

    @Slot()
    def on_target_1_set(self):
        self.qt_controller.set_screw_target(1)

    @Slot()
    def on_target_2_set(self):
        self.qt_controller.set_screw_target(2)

    @Slot()
    def on_target_3_set(self):
        self.qt_controller.set_screw_target(3)

    @Slot()
    def on_target_4_set(self):
        self.qt_controller.set_screw_target(4)

    @Slot()
    def on_target_5_set(self):
        self.qt_controller.set_screw_target(5)

    @Slot()
    def on_target_6_set(self):
        self.qt_controller.set_screw_target(6)

    @Slot()
    def on_target_7_set(self):
        self.qt_controller.set_screw_target(7)

    @Slot()
    def on_target_8_set(self):
        self.qt_controller.set_screw_target(8)

    @Slot()
    def on_target_reset_set(self):
        self.qt_controller.set_screw_target(0)


class HardwareSettingWidget(QGroupBox):
    def __init__(self, qt_controller: QtController):
        super().__init__("硬件设置")

        self.qt_controller = qt_controller

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        hardware_form = QFormLayout()

        # 分辨率
        self.resolution_combo = QComboBox()
        resolution_options = ["0.2", "0.4", "0.8", "1.0", "2.0"]
        self.resolution_combo.addItems(resolution_options)
        self.resolution_combo.setCurrentText("0.4")
        hardware_form.addRow(QLabel("分辨率:"), self.resolution_combo)

        # 动镜速度
        self.velocity_combo = QComboBox()
        velocity_options = ["200", "300", "500", "1000", "2000", "3000"]
        self.velocity_combo.addItems(velocity_options)
        self.velocity_combo.setCurrentText("300")
        hardware_form.addRow(QLabel("动镜速度:"), self.velocity_combo)

        # 采样方向
        self.direction_combo = QComboBox()
        direction_options = ["正向", "反向"]
        self.direction_combo.addItems(direction_options)
        self.direction_combo.setCurrentText("正向")
        hardware_form.addRow(QLabel("采样方向:"), self.direction_combo)

        # 扫描模式
        self.scan_mode_combo = QComboBox()
        scan_mode_options = ["单向-单边", "单向-双边", "双向-单边", "双向-双边"]
        self.scan_mode_combo.addItems(scan_mode_options)
        self.scan_mode_combo.setCurrentText("单向-单边")
        hardware_form.addRow(QLabel("扫描模式:"), self.scan_mode_combo)

        main_layout.addLayout(hardware_form)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

    def setup_signals(self):
        self.save_button.clicked.connect(self.on_save_settings)

    @Slot()
    def on_save_settings(self):
        # 保存设置
        pass


class ControlWidget(QWidget):
    def __init__(self, qt_controller: QtController):
        super().__init__()
        self.qt_controller = qt_controller

        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Add communication widget
        self.comm_widget = CommunicationWidget(self.qt_controller)
        main_layout.addWidget(self.comm_widget)

        light_widget = LightWidget(self.qt_controller)
        main_layout.addWidget(light_widget)

        rotate_widget = RotateMotorWidget(self.qt_controller)
        main_layout.addWidget(rotate_widget)

        screw_widget = ScrewMotorWidget(self.qt_controller)
        main_layout.addWidget(screw_widget)

        hardware_widget = HardwareSettingWidget(self.qt_controller)
        main_layout.addWidget(hardware_widget)

        # Add collect widget
        self.collect_widget = CollectWidget()
        self.collect_widget.data_collected.connect(
            self.on_data_collected
        )  # 连接采集数据信号

        # Add widgets to main layout

        main_layout.addWidget(self.collect_widget)
        main_layout.addStretch()

    @Slot()
    def on_check_start(self):
        pass

    @Slot()
    def on_check_stop(self):
        pass

    @Slot(list, list)
    def on_data_collected(self, x_data, y_data):
        """处理采集到的数据并更新图表"""
        self.figure_widget.update_data(x_data, y_data)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from config.log import setup_logging

    setup_logging()

    app = QApplication(sys.argv)
    qt_controller = QtController()  # 创建 QtController 实例
    widget = ControlWidget(qt_controller=qt_controller)
    widget.show()
    app.exit(app.exec())
