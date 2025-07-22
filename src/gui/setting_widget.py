from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QWidget,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QSpinBox,
    QHBoxLayout,
    QRadioButton,
)
from PySide6.QtCore import Qt

from comm.manager import CommManager


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
        hardware_form.addRow(QLabel("硬件参数1:"), QLineEdit())
        hardware_form.addRow(QLabel("硬件参数2:"), QLineEdit())
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
        communication_form.addRow(QLabel("通信端口:"), QLineEdit())
        communication_form.addRow(QLabel("波特率:"), QComboBox())
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

    def save_settings(self):
        # Placeholder for saving settings logic
        print("Settings saved!")
        self.accept()
