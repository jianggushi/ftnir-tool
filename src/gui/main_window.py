from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QStatusBar,
    QMenuBar,
    QMenu,
    QMessageBox,
    QSplitter,
    QLabel,
    QPushButton,
    QTextEdit,
)
from PySide6.QtCore import Qt

from comm.manager import CommManager
from .control_widget import ControlWidget
from .interference_widget import InterferenceFigureWidget
from .spectrum_figure import SpectrumFigureWidget
from .setting_widget import (
    HardwareSettingWidget,
    CollectSettingWidget,
    CommunicationSettingWidget,
)


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

        settings_menu = QMenu("设置", self)
        menu_bar.addMenu(settings_menu)

        menu_bar.addMenu(QMenu("帮助", self))
        # Define menu actions and their corresponding methods

        menu_actions = [
            ("硬件设置", self.open_hardware_settings),
            ("采集设置", self.open_acquisition_settings),
            ("通信设置", self.open_communication_settings),
        ]

        # Add actions to the menu
        for action_name, method in menu_actions:
            action = settings_menu.addAction(action_name)
            action.triggered.connect(method)

    def open_hardware_settings(self):
        # Create and show the hardware settings dialog
        hardware_dialog = HardwareSettingWidget(self)
        # hardware_dialog.tab_widget.setCurrentIndex(0)  # Select "硬件设置" tab
        hardware_dialog.exec()

    def open_acquisition_settings(self):
        # Create and show the acquisition settings dialog
        acquisition_dialog = CollectSettingWidget(self)
        # acquisition_dialog.tab_widget.setCurrentIndex(1)  # Select "采集设置" tab
        acquisition_dialog.exec()

    def open_communication_settings(self):
        # Create and show the communication settings dialog
        communication_dialog = CommunicationSettingWidget(self)
        # communication_dialog.tab_widget.setCurrentIndex(2)  # Select "通信设置" tab
        communication_dialog.exec()

    def setup_status_bar(self):
        pass
