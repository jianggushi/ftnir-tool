from PySide6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from matplotlib import rcParams

from comm.manager import CommManager
from comm.protocol.command import Command
from comm.handler.spectrum import SpectrumHandler


class SpectrumFigureWidget(QWidget):
    def __init__(self, comm_manager: CommManager):

        # 设置中文字体
        rcParams["font.family"] = ["Microsoft YaHei", "SimHei"]
        rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

        super().__init__()
        self.setup_ui()
        self._init_plot()

        self.comm_manager = comm_manager
        # 创建消息处理器
        self._spectrum_handler = SpectrumHandler()
        self._spectrum_handler.set_callback(self.on_receive_spectrum_data)
        self.comm_manager.register_handler(Command.CHECK_RESP, self._spectrum_handler)

        # 数据缓存
        self._x_data = []
        self._y_data = []

    def setup_ui(self):
        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # 创建matplotlib画布
        self.figure = Figure(figsize=(8, 6), tight_layout=True)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

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
        # self.ax.set_xlim(0, 1000)  # 默认显示前1000个数据点
        # self.ax.set_ylim(-1.0, 1.0)  # 根据信号强度合理范围设定
        # self.ax.set_title("FTIR数据")
        self.ax.set_xlabel("波数")
        self.ax.set_ylabel("光谱图强度")
        # self.ax.grid(True)

        # 创建空的线条对象
        (self.line,) = self.ax.plot([], [], "b-")
        # self.ax.legend()

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

        # 自动调整坐标轴范围
        self.ax.relim(visible_only=True)
        self.ax.autoscale_view(scalex=True, scaley=True, tight=True)

        # 设置新的x轴范围
        if len(self._x_data) > 0:
            self.ax.set_xlim(min(self._x_data), max(self._x_data))

        # 重绘画布
        self.canvas.draw()

    def clear_plot(self):
        """清空图表"""
        self._x_data = []
        self._y_data = []
        self.line.set_data([], [])
        self.canvas.draw()

    def on_receive_spectrum_data(self, data: list[float]):
        """处理接收到的光谱数据"""
        x_data = list(range(len(data)))
        self.update_data(x_data, data)


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = SpectrumFigureWidget()
    widget.show()

    # 测试数据
    x = np.linspace(400, 4000, 1000)
    y = np.sin(x / 100) + np.random.random(1000) * 0.1
    widget.update_data(x, y)

    sys.exit(app.exec())
