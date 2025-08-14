import numpy as np
from PySide6.QtWidgets import (
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QTabWidget,
    QWidget,
    QGroupBox,
)
from PySide6.QtCore import Slot

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from util.util import init_font

from interfaces.qt.controller import QtController
from core.model.spectrum import LightStabilityData


class LightStabilityWidget(QWidget):
    def __init__(self, qt_controller: QtController):
        super().__init__()

        self.qt_controller = qt_controller
        self.qt_controller.light_stability_handler.add_callback(
            self.on_receive_interference_data
        )

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        top_widget = self.create_top_widget()
        main_layout.addWidget(top_widget, 0)

        down_widget = QTabWidget()
        down_widget.addTab(self.create_chart_tab(), "图表")
        # down_widget.addTab(self.create_data_tab(), "数据")

        main_layout.addWidget(down_widget, 1)

    def setup_signals(self):
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)

    def create_top_widget(self) -> QWidget:
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)

        top_layout.addWidget(self.create_result_group())
        top_layout.addWidget(self.create_control_group())

        return top_widget

    def create_result_group(self) -> QGroupBox:
        result_group = QGroupBox("测量结果")
        result_layout = QFormLayout()
        result_group.setLayout(result_layout)

        self.max_max_label = QLabel("0.0")
        result_layout.addRow(QLabel("Max最大强度:"), self.max_max_label)

        self.min_max_label = QLabel("0.0")
        result_layout.addRow(QLabel("Min最大强度:"), self.min_max_label)

        # self.avg_max_label = QLabel("0.0")
        # result_layout.addRow(QLabel("Avg最大强度:"), self.avg_max_label)

        # self.std_max_label = QLabel("0.0")
        # result_layout.addRow(QLabel("标准差:"), self.std_max_label)

        return result_group

    def create_control_group(self) -> QGroupBox:
        control_group = QGroupBox("控制")
        control_layout = QVBoxLayout()
        control_group.setLayout(control_layout)

        self.start_button = QPushButton("开始测量")
        self.stop_button = QPushButton("停止测量")
        self.save_button = QPushButton("保存数据")

        self.stop_button.setEnabled(False)

        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.save_button)

        return control_group

    def create_chart_tab(self) -> QWidget:
        chart_tab = QWidget()
        chart_layout = QVBoxLayout(chart_tab)

        self.interference_widget = InterferenceFigureWidget(self.qt_controller)

        chart_layout.addWidget(self.interference_widget)

        return chart_tab

    # def create_data_tab(self) -> QWidget:
    #     data_tab = QWidget()
    #     data_layout = QVBoxLayout(data_tab)

    #     # 数据表格
    #     self.light_table = QTableWidget()
    #     self.light_table.setColumnCount(3)
    #     self.light_table.setHorizontalHeaderLabels(["时间", "强度", "状态"])
    #     self.light_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #     data_layout.addWidget(self.light_table)

    #     return data_tab

    @Slot()
    def on_start(self):
        self.qt_controller.check_light_stability()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    @Slot()
    def on_stop(self):
        self.qt_controller.check_stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def on_receive_interference_data(self, data: LightStabilityData):
        # TODO: 数据类型转换可能有问题
        interference_data = data.interference
        x_data = list(range(interference_data.shape[0]))
        self.max_max_label.setText(f"{data.max_max:.6f}")
        self.min_max_label.setText(f"{data.min_max:.6f}")
        # self.avg_max_label.setText(f"{data.avg_max:.6f}")
        # self.std_max_label.setText(f"{data.std_max:.6f}")
        self.interference_widget.update_data(x_data, interference_data.tolist())
        self.interference_widget.update_max_max(data.max_max)


class InterferenceFigureWidget(QWidget):

    def __init__(self, qt_controller: QtController):
        super().__init__()
        init_font()

        self.qt_controller = qt_controller

        # 数据缓存
        self._x_data = []
        self._y_data = []
        self._x_min = 0
        self._x_max = 1
        self._y_min = 0
        self._y_max = 2

        self.ref_max = 1.9

        self.setup_ui()
        self._init_plot()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        self.figure = Figure(figsize=(8, 6), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)

        toolbar = NavigationToolbar(self.canvas, self)

        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.canvas)

    def _init_plot(self):
        """初始化绘图"""
        self.ax = self.figure.add_subplot(1, 1, 1)
        # 调整布局参数使图表充满画布
        self.figure.subplots_adjust(
            left=0.05,  # 左边距从默认0.125缩小
            right=0.98,  # 右边距从默认0.9增大
            top=0.95,  # 上边距从默认0.88缩小
            bottom=0.05,  # 下边距从默认0.11缩小
            hspace=0,  # 水平间距清零
            wspace=0,  # 垂直间距清零
        )
        # 设置初始坐标范围
        self.ax.set_xlim(self._x_min, self._x_max)
        self.ax.set_ylim(self._y_min, self._y_max)

        # self.ax.set_title("FTIR数据")
        self.ax.set_xlabel("数据点")
        self.ax.set_ylabel("干涉图强度")
        # self.ax.grid(True)

        # 创建空的线条对象
        (self.line,) = self.ax.plot([], [], "b-")
        self.ref_max_line = self.ax.axhline(
            y=self.ref_max, color="red", linestyle="--", linewidth=2, label="y=0"
        )
        self.max_max_line = self.ax.axhline(
            y=0, color="blue", linestyle="--", linewidth=2, label="y=0"
        )

    def update_data(self, x_data, y_data):
        """更新数据并重绘

        Args:
            x_data: x轴数据（波数）
            y_data: y轴数据（透过率）
        """
        # 更新数据
        self._x_data = x_data
        self._y_data = y_data

        # 更新线条数据
        self.line.set_data(self._x_data, self._y_data)

        self._x_max = max(max(self._x_data), self._x_max)
        self._x_min = min(min(self._x_data), self._x_min)
        self._y_max = max(max(self._y_data), self._y_max)
        self._y_min = min(min(self._y_data), self._y_min)
        self.ax.set_xlim(self._x_min, self._x_max)
        self.ax.set_ylim(self._y_min, self._y_max)

        # 重绘画布
        self.canvas.draw()

    def update_max_max(self, max_max):
        self.max_max_line.set_ydata([max_max, max_max])

    def clear_plot(self):
        """清空图表"""
        self._x_data = []
        self._y_data = []
        self.line.set_data([], [])
        self.canvas.draw()
