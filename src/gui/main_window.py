from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMenu,
    QSplitter,
)
from PySide6.QtCore import Qt

from handler.manager import CommManager
from .control_widget import ControlWidget
from .interference_widget import InterferenceFigureWidget
from .spectrum_figure import SpectrumFigureWidget
from .setting_widget import (
    HardwareSettingWidget,
    CollectSettingWidget,
    CommunicationSettingWidget,
)
from .signal_widget2 import SignalWidget


class MainWindow(QMainWindow):
    def __init__(self):
        self.comm_manager = CommManager()

        super().__init__()
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()

    def setup_ui(self):
        # Set window title and size
        self.setWindowTitle("光谱上位机系统")
        self.resize(1200, 800)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Add control widget (left panel)
        self.control_widget = ControlWidget(self.comm_manager)
        self.control_widget.setMinimumWidth(200)  # Set minimum width
        splitter.addWidget(self.control_widget)

        # Create vertical layout for right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Add interference widget (top of right panel)
        self.interference_widget = InterferenceFigureWidget(self.comm_manager)
        right_layout.addWidget(self.interference_widget)

        # Add spectrum widget (bottom of right panel)
        self.spectrum_widget = SpectrumFigureWidget(self.comm_manager)
        right_layout.addWidget(self.spectrum_widget)

        splitter.addWidget(right_panel)

        # Set initial splitter sizes (30% left, 70% right)
        splitter.setSizes([200, 800])

    def setup_menu(self):
        # Create menu bar
        menu_bar = self.menuBar()
        menu_bar.setStyleSheet("background-color: white;")

        menu_bar.addMenu(QMenu("文件", self))

        # Create settings menu
        settings_menu = QMenu("设置", self)
        menu_bar.addMenu(settings_menu)

        menu_actions = [
            ("硬件设置", self.open_hardware_settings),
            ("采集设置", self.open_acquisition_settings),
            ("通信设置", self.open_communication_settings),
        ]
        # Add actions to the settings menu
        for action_name, method in menu_actions:
            action = settings_menu.addAction(action_name)
            action.triggered.connect(method)

        self.hardware_dialog = HardwareSettingWidget(self)
        self.acquisition_dialog = CollectSettingWidget(self)
        self.communication_dialog = CommunicationSettingWidget(self.comm_manager)

        # Create signal menu
        signal_menu = QMenu("信号", self)
        menu_bar.addMenu(signal_menu)

        signal_menu.addAction("信号检查", self.open_signal_widget)
        self.signal_widget = SignalWidget(self.comm_manager)

        # Create help menu
        menu_bar.addMenu(QMenu("帮助", self))

    def open_hardware_settings(self):
        self.hardware_dialog.exec()

    def open_acquisition_settings(self):
        self.acquisition_dialog.exec()

    def open_communication_settings(self):
        self.communication_dialog.exec()

    def open_signal_widget(self):
        self.signal_widget.exec()

    def setup_status_bar(self):
        pass
