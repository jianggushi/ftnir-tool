from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import rcParams


class BaseInterferenceWidget(QWidget):

    def __init__(self):
        # 设置中文字体
        rcParams["font.family"] = ["Microsoft YaHei", "SimHei"]
        rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

        super().__init__()

        # 数据缓存
        self._x_data = []
        self._y_data = []
        self._x_min = 0
        self._x_max = 1
        self._y_min = 0
        self._y_max = 1

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
