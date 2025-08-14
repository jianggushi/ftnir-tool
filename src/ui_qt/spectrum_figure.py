import numpy as np
from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from core.model.spectrum import SpectrumData

from util.util import init_font


class SpectrumFigureWidget(QWidget):

    def __init__(self):
        super().__init__()
        init_font()

        self.setup_ui()
        self.init_plot()

        # 数据缓存
        self._x_data = []
        self._y_data = []

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
        self.ax = self.figure.add_subplot(2, 1, 1)
        self.ax.set_xlabel("数据点")
        self.ax.set_ylabel("干涉图强度")

        self.bx = self.figure.add_subplot(2, 1, 2)
        self.bx.set_xlabel("波数")
        self.bx.set_ylabel("光谱图强度")

        # 设置初始坐标范围
        # self.ax.set_xlim(0, 1000)  # 默认显示前1000个数据点
        # self.ax.set_ylim(-1.0, 1.0)  # 根据信号强度合理范围设定
        # self.ax.set_title("FTIR数据")

        # 创建空的线条对象
        (self.aline,) = self.ax.plot([], [], "b-")
        (self.bline,) = self.bx.plot([], [], "b-")

    def update_aline(self, x_data, y_data):
        """更新数据并重绘

        Args:
            x_data: x轴数据（波数）
            y_data: y轴数据（透过率）
        """
        # 更新数据
        self._x_data = x_data
        self._y_data = y_data

        # 更新线条数据
        self.aline.set_data(self._x_data, self._y_data)

        # 自动调整坐标轴范围
        self.ax.relim(visible_only=True)
        self.ax.autoscale_view(scalex=True, scaley=True, tight=True)

        # 设置新的x轴范围
        if len(self._x_data) > 0:
            self.ax.set_xlim(min(self._x_data), max(self._x_data))

        # 重绘画布
        self.canvas.draw()

    def update_bline(self, x_data, y_data):
        """更新数据并重绘

        Args:
            x_data: x轴数据（波数）
            y_data: y轴数据（透过率）
        """
        # 更新数据
        self._x_data = x_data
        self._y_data = y_data

        # 更新线条数据
        self.bline.set_data(self._x_data, self._y_data)

        # 自动调整坐标轴范围
        self.bx.relim(visible_only=True)
        self.bx.autoscale_view(scalex=True, scaley=True, tight=True)

        # 设置新的x轴范围
        if len(self._x_data) > 0:
            self.bx.set_xlim(min(self._x_data), max(self._x_data))

        # 重绘画布
        self.canvas.draw()

    def clear_plot(self):
        """清空图表"""
        self._x_data = []
        self._y_data = []
        self.aline.set_data([], [])
        self.canvas.draw()

    def on_receive_data(self, data: SpectrumData):
        interference_data = data.interference
        x_data = list(range(interference_data.shape[0]))
        self.update_aline(x_data, interference_data.tolist())
        spectrum_data = data.spectrum
        x_data = list(range(spectrum_data.shape[0]))
        self.update_bline(x_data, spectrum_data.tolist())


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
