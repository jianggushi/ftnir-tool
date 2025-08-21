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


class HardwareSettingWidget(QGroupBox):
    def __init__(self):
        super().__init__("硬件设置")

        self.setup_ui()

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

    def get_settings(self):
        # TODO:jxj
        pass
