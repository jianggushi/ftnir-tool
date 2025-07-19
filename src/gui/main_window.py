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

from .control_widget import ControlWidget
from .figure_widget import FigureWidget
from comm.manager import CommManager


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

        # Add figure widget (right panel)
        self.figure_widget = FigureWidget(self.comm_manager)
        splitter.addWidget(self.figure_widget)

        # Set initial splitter sizes (30% left, 70% right)
        splitter.setSizes([200, 800])

    def setup_menu(self):
        pass

    def setup_status_bar(self):
        pass
