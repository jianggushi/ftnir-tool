from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QRadioButton,
)

from handler.manager import CommManager


class HardwareSettingWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("硬件设置")
        self.resize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Hardware settings form
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

        # Connect buttons
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)

    def save_settings(self):
        # Placeholder for saving settings logic
        resolution = self.resolution_combo.currentText()
        velocity = self.velocity_combo.currentText()
        direction = self.direction_combo.currentText()
        scan_mode = self.scan_mode_combo.currentText()
        print("Settings saved!")
        self.accept()


class CollectSettingWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("采集设置")
        self.resize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Acquisition settings form
        acquisition_form = QFormLayout()

        # 采集模式选择
        self.single_radio = QRadioButton("单次采集")
        self.continuous_radio = QRadioButton("连续采集")
        self.single_radio.setChecked(True)
        acquisition_form.addRow(QLabel("采集模式:"), self.single_radio)
        acquisition_form.addRow("", self.continuous_radio)

        # 采集次数设置
        self.count_label = QLabel("采集次数:")
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("输入采集次数")
        acquisition_form.addRow(self.count_label, self.count_input)

        main_layout.addLayout(acquisition_form)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        # Connect buttons
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)

        # Connect radio buttons
        self.single_radio.toggled.connect(self.on_mode_change)

    def on_mode_change(self):
        """根据采集模式启用或禁用采集次数输入框"""
        self.count_input.setEnabled(self.single_radio.isChecked())

    def save_settings(self):
        # Placeholder for saving settings logic
        print("Settings saved!")
        self.accept()


class CommunicationSettingWidget(QDialog):
    def __init__(self, comm_manager: CommManager):
        self.comm_manager = comm_manager
        super().__init__()
        self.setWindowTitle("通信设置")
        self.resize(600, 400)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout(self)

        # Communication settings form
        communication_form = QFormLayout()

        self.port_combo = QComboBox()
        self.refresh_button = QPushButton("刷新")

        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_combo)
        port_layout.addWidget(self.refresh_button)

        communication_form.addRow(QLabel("通信端口:"), port_layout)
        main_layout.addLayout(communication_form)

        # Buttons
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("保存")
        self.cancel_button = QPushButton("取消")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        # Connect buttons
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button.clicked.connect(self.reject)
        self.refresh_button.clicked.connect(self.refresh_ports)

    def refresh_ports(self):
        self.port_combo.clear()
        ports = self.comm_manager.list_ports()
        self.port_combo.addItems(ports)

    def save_settings(self):
        # Placeholder for saving settings logic
        port = self.port_combo.currentText()
        self.comm_manager.transport.set_port(port)
        self.accept()
