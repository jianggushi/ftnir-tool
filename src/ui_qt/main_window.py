from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMenu,
    QSplitter,
)
from PySide6.QtCore import Qt

from .control_widget import ControlWidget
from .spectrum_figure import SpectrumFigureWidget
from .setting_widget import (
    HardwareSettingWidget,
    CollectSettingWidget,
    CommunicationSettingWidget,
)
from .light_stability_widget import LightStabilityWidget
from .wave_accuracy_widget import WaveAccuracyWidget
from .wave_repeatability_widget import WaveRepeatabilityWidget
from .log_widget import LogWidget
from .status_bar import StatusBarWidget


class MainWindow(QMainWindow):
    def __init__(self):
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
        self.control_widget = ControlWidget()
        self.control_widget.setMinimumWidth(200)  # Set minimum width
        splitter.addWidget(self.control_widget)

        # Create vertical layout for right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        # Add spectrum widget (top of right panel)
        self.spectrum_widget = SpectrumFigureWidget()
        right_layout.addWidget(self.spectrum_widget)

        # Add spectrum widget (bottom of right panel)
        # self.spectrum_widget = SpectrumFigureWidget(self.qt_controller)
        # right_layout.addWidget(self.spectrum_widget)

        splitter.addWidget(right_panel)

        # Set initial splitter sizes (30% left, 70% right)
        splitter.setSizes([220, 780])

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
        self.communication_dialog = CommunicationSettingWidget()

        # Create signal menu
        signal_menu = QMenu("信号", self)
        menu_bar.addMenu(signal_menu)

        # signal_menu.addAction("信号检查", self.open_signal_widget)
        # self.signal_widget = SignalCheckWidget()

        signal_menu.addAction("光源稳定性", self.open_light_stability_widget)
        self.light_stability_widget = LightStabilityWidget()

        signal_menu.addAction("波数准确性", self.open_wave_accuracy_widget)
        self.wave_accuracy_widget = WaveAccuracyWidget()

        signal_menu.addAction("波数重复性", self.open_wave_repeatability_widget)
        self.wave_repeatability_widget = WaveRepeatabilityWidget()

        tool_menu = QMenu("工具", self)
        menu_bar.addMenu(tool_menu)
        tool_menu.addAction("日志", self.open_log_widget)
        self.log_widget = LogWidget()

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

    def open_light_stability_widget(self):
        self.light_stability_widget.show()

    def open_wave_accuracy_widget(self):
        self.wave_accuracy_widget.show()

    def open_wave_repeatability_widget(self):
        self.wave_repeatability_widget.show()

    def open_log_widget(self):
        self.log_widget.show()

    def setup_status_bar(self):
        self.status_bar = StatusBarWidget()
        self.setStatusBar(self.status_bar)
