from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QProgressBar,
    QRadioButton,
    QButtonGroup,
)

from PySide6.QtCore import Slot, Signal


class SignalCheckWidget(QGroupBox):
    # 定义信号
    check_started = Signal()  # 请求检查信号
    check_stopped = Signal()  # 请求停止检查

    def __init__(self, parent=None):
        super().__init__("信号检查", parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create button group for radio buttons
        self.check_group = QButtonGroup(self)

        # 光源稳定性检查
        stability_layout = QHBoxLayout()
        self.stability_radio = QRadioButton("光源稳定性")
        self.stability_radio.setChecked(True)  # Default selection
        stability_layout.addWidget(self.stability_radio)
        self.check_group.addButton(self.stability_radio)

        # 波长准确性检查
        accuracy_layout = QHBoxLayout()
        self.accuracy_radio = QRadioButton("波长准确性")
        accuracy_layout.addWidget(self.accuracy_radio)
        self.check_group.addButton(self.accuracy_radio)

        # 波长重复性检查
        repeatability_layout = QHBoxLayout()
        self.repeatability_radio = QRadioButton("波长重复性")
        repeatability_layout.addWidget(self.repeatability_radio)
        self.check_group.addButton(self.repeatability_radio)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 开始检查按钮
        self.start_btn = QPushButton("开始检查")
        self.start_btn.clicked.connect(self.start_check)

        # 停止检查按钮
        self.stop_btn = QPushButton("停止检查")
        self.stop_btn.clicked.connect(self.stop_check)
        self.stop_btn.setEnabled(False)

        # 添加按钮到布局
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)

        # Add all layouts to main layout
        layout.addLayout(stability_layout)
        layout.addLayout(accuracy_layout)
        layout.addLayout(repeatability_layout)
        layout.addLayout(button_layout)

    @Slot()
    def start_check(self):
        """开始检查"""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self._is_checking = True

        # 获取检查类型并发送信号
        check_type = ""
        if self.stability_radio.isChecked():
            check_type = "stability"
        elif self.accuracy_radio.isChecked():
            check_type = "accuracy"
        elif self.repeatability_radio.isChecked():
            check_type = "repeatability"

        self.check_started.emit(check_type)

    @Slot()
    def stop_check(self):
        """停止检查"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self._is_checking = False
        self.check_stopped.emit()
