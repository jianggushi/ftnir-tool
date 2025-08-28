import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

from config.types import CollectData

from util.util import init_font


class SpectrumFigureWidget(QWidget):

    def __init__(self):
        super().__init__()
        init_font()

        self.show_ax = True
        self.show_bx = True
        # 数据缓存
        self._ax_data = []
        self._ay_data = []
        self._bx_data = []
        self._by_data = []

        self.setup_ui()
        self.init_plot()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # 创建matplotlib画布
        self.figure = Figure(figsize=(8, 6), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)

        toolbar = NavigationToolbar(self.canvas, self)

        main_layout.addWidget(toolbar)
        main_layout.addWidget(self.canvas)

    def init_plot(self):
        self.gs = GridSpec(2, 1, figure=self.figure)

        self.ax = self.figure.add_subplot(self.gs[0])
        self.ax.set_xlabel("数据点")
        self.ax.set_ylabel("干涉图强度")

        self.bx = self.figure.add_subplot(self.gs[1])
        self.bx.set_xlabel("波数")
        self.bx.set_ylabel("光谱图强度")

        self.ax_spec = self.ax.get_subplotspec()
        self.bx_spec = self.bx.get_subplotspec()
        self.full_spec = self.gs[:]

        # 设置初始坐标范围
        self.ax.set_xlim(0, 1000)
        self.bx.set_xlim(12000, 4000)

        # 创建空的线条对象
        (self.aline,) = self.ax.plot([], [], "b-", linewidth=1.0)
        (self.bline,) = self.bx.plot([], [], "b-", linewidth=1.0)

    def update_aline(self, x_data, y_data):
        # 更新数据
        self._ax_data = x_data
        self._ay_data = y_data

        # 更新线条数据
        self.aline.set_data(self._ax_data, self._ay_data)

        # 自动调整坐标轴范围
        self.ax.relim(visible_only=True)
        self.ax.autoscale_view(scalex=True, scaley=True, tight=True)

        # 设置新的x轴范围
        if len(self._ax_data) > 0:
            self.ax.set_xlim(min(self._ax_data), max(self._ax_data))

        # 重绘画布
        self.canvas.draw()

    def update_bline(self, x_data, y_data):
        # 更新数据
        self._bx_data = x_data
        self._by_data = y_data

        # 更新线条数据
        self.bline.set_data(self._bx_data, self._by_data)

        # 自动调整坐标轴范围
        self.bx.relim(visible_only=True)
        self.bx.autoscale_view(scalex=True, scaley=True, tight=True)

        # 设置新的x轴范围
        if len(self._bx_data) > 0:
            self.bx.set_xlim(max(self._bx_data), min(self._bx_data))

        # 重绘画布
        self.canvas.draw()

    def clear_plot(self):
        """清空图表"""
        self._ax_data = []
        self._ay_data = []
        self._bx_data = []
        self._by_data = []
        self.aline.set_data([], [])
        self.bline.set_data([], [])
        self.canvas.draw()

    def on_receive_data(self, data: CollectData):
        interference_data = data.interference_data
        x_data = list(range(interference_data.shape[0]))
        self.update_aline(x_data, interference_data.tolist())

        spectrum_data = data.spectrum_data
        x_data = data.freq_data
        self.update_bline(x_data.tolist(), spectrum_data.tolist())

    def show_ax_or_bx(self, show_ax: bool, show_bx: bool):
        self.show_ax = show_ax
        self.show_bx = show_bx
        self.ax.set_visible(show_ax)
        self.bx.set_visible(show_bx)
        if self.show_ax and show_bx:
            self.ax.set_subplotspec(self.ax_spec)
            self.bx.set_subplotspec(self.bx_spec)
        elif self.show_ax:
            self.ax.set_subplotspec(self.full_spec)
        elif self.show_bx:
            self.bx.set_subplotspec(self.full_spec)
        else:
            pass
        self.canvas.draw()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = SpectrumFigureWidget()
    widget.show()

    # # 测试数据
    # x = np.linspace(400, 4000, 1000)
    # y = np.sin(x / 100) + np.random.random(1000) * 0.1
    # widget.update_data(x, y)

    sys.exit(app.exec())
