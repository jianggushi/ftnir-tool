import enum

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

from config.types import (
    ResolutionEnum,
    VelocityEnum,
    DirectionEnum,
    ScanModeEnum,
    HardwareData,
)


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
        resolution_options = [item.label for item in ResolutionEnum]
        self.resolution_combo.addItems(resolution_options)
        self.resolution_combo.setCurrentText(ResolutionEnum.R_8_0.label)
        hardware_form.addRow(QLabel("分辨率:"), self.resolution_combo)

        # 动镜速度
        self.velocity_combo = QComboBox()
        velocity_options = [item.label for item in VelocityEnum]
        self.velocity_combo.addItems(velocity_options)
        self.velocity_combo.setCurrentText(VelocityEnum.V_300.label)
        hardware_form.addRow(QLabel("动镜速度:"), self.velocity_combo)

        # 采样方向
        self.direction_combo = QComboBox()
        direction_options = [item.label for item in DirectionEnum]
        self.direction_combo.addItems(direction_options)
        self.direction_combo.setCurrentText(DirectionEnum.D_P.label)
        hardware_form.addRow(QLabel("采样方向:"), self.direction_combo)

        # 扫描模式
        self.scan_mode_combo = QComboBox()
        scan_mode_options = [item.label for item in ScanModeEnum]
        self.scan_mode_combo.addItems(scan_mode_options)
        self.scan_mode_combo.setCurrentText(ScanModeEnum.S_2.label)
        hardware_form.addRow(QLabel("扫描模式:"), self.scan_mode_combo)

        main_layout.addLayout(hardware_form)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

    def get_settings(self) -> HardwareData:
        resolution = self.resolution_combo.currentText()
        speed = self.velocity_combo.currentText()
        direction = self.direction_combo.currentText()
        scan_mode = self.scan_mode_combo.currentText()

        return HardwareData(
            resolution=ResolutionEnum.from_label(resolution).value,
            velocity=VelocityEnum.from_label(speed).value,
            direction=DirectionEnum.from_label(direction).value,
            scan_mode=ScanModeEnum.from_label(scan_mode).value,
        )
