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

from core.model.spectrum import HardwareData


class ResolutionEnum(enum.Enum):
    R_0_2 = (1, "0.2")
    R_0_4 = (2, "0.4")
    R_0_8 = (3, "0.8")
    R_1_0 = (4, "1.0")
    R_2_0 = (5, "2.0")

    def __init__(self, num, label):
        self._value_ = num
        self.label = label

    @classmethod
    def from_label(cls, label: str):
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"{label!r} is not a valid {cls.__name__}")


class VelocityEnum(enum.Enum):
    V_200 = (1, "200")
    V_300 = (2, "300")
    V_500 = (3, "500")
    V_1000 = (4, "1000")
    V_2000 = (5, "2000")
    V_3000 = (6, "3000")

    def __init__(self, num, label):
        self._value_ = num
        self.label = label

    @classmethod
    def from_label(cls, label: str):
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"{label!r} is not a valid {cls.__name__}")


class ScanModeEnum(enum.Enum):
    S_1 = (1, "单向-单边")
    S_2 = (2, "单向-双边")
    S_3 = (3, "双向-单边")
    S_4 = (4, "双向-双边")

    def __init__(self, num, label):
        self._value_ = num
        self.label = label

    @classmethod
    def from_label(cls, label: str):
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"{label!r} is not a valid {cls.__name__}")


class DirectionEnum(enum.Enum):
    D_P = (1, "正向")
    D_N = (2, "反向")

    def __init__(self, num, label):
        self._value_ = num
        self.label = label

    @classmethod
    def from_label(cls, label: str):
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"{label!r} is not a valid {cls.__name__}")


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
        self.resolution_combo.setCurrentText(ResolutionEnum.R_0_4.label)
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
