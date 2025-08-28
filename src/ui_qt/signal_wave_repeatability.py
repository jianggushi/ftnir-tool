import numpy as np
from PySide6.QtWidgets import (
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QTabWidget,
    QWidget,
    QDialog,
)
from PySide6.QtCore import Slot, Signal


from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from util.util import init_font

from config.types import LightStabilityData


class WaveRepeatabilityWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("波数重复性检查")

        self.resize(1200, 800)

        self.light_stability_data: LightStabilityData = None

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        top_widget = self.create_top_widget()
        main_layout.addWidget(top_widget, 0)

        down_widget = QTabWidget()
        self.spectrum_figure = SpectrumFigure()
        down_widget.addTab(self.spectrum_figure, "光谱图")

        main_layout.addWidget(down_widget, 1)

    def create_top_widget(self) -> QWidget:
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.addStretch()

        self.start_button = QPushButton("开始检查")
        self.stop_button = QPushButton("停止检查")
        self.stop_button.setEnabled(False)

        top_layout.addWidget(self.start_button)
        top_layout.addWidget(self.stop_button)

        self.save_button = QPushButton("保存数据")
        top_layout.addWidget(self.save_button)

        return top_widget

    @Slot(object)
    def on_receive_data(self, data: LightStabilityData):
        self.light_stability_data = data

        spectrum_data = data.spectrum_data
        x_data = list(range(spectrum_data.shape[0]))
        self.spectrum_figure.update_data(
            x_data, spectrum_data.tolist(), data.spectrum_max_max
        )

        # self.interference_figure.max_max_label.setText(
        #     f"{data.interference_max_max:.6f}"
        # )


class SpectrumFigure(QWidget):
    def __init__(self):
        super().__init__()
        init_font()

        self._x_data = []
        self._y_data = []

        self._x_min = 0
        self._x_max = 1
        self._y_min = 0
        self._y_max = 0

        self.ref_max = 0

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
        main_layout.addWidget(self.canvas, stretch=1)

    def _init_plot(self):
        """初始化绘图"""
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.set_xlabel("波数")
        self.ax.set_ylabel("光谱图强度")

        # 设置初始坐标范围
        self.ax.set_xlim(self._x_min, self._x_max)
        self.ax.set_ylim(self._y_min, self._y_max)

        # 创建空的线条对象
        (self.aline,) = self.ax.plot([], [], "b-")
        self.ref_max_line = self.ax.axhline(
            y=self.ref_max, color="red", linestyle="--", label="参考最大强度"
        )
        self.max_max_line = self.ax.axhline(
            y=0, color="blue", linestyle="--", label="当前最大强度"
        )

    def set_ref_max(self, ref_max: float):
        self.ref_max = ref_max
        self.ref_max_line.set_ydata([ref_max, ref_max])
        self.canvas.draw()

    def update_data(self, x_data: list[float], y_data: list[float], max_max: float):
        """更新数据并重绘"""
        # 更新数据
        self._x_data = x_data
        self._y_data = y_data

        # 更新线条数据
        self.aline.set_data(self._x_data, self._y_data)
        self.max_max_line.set_ydata([max_max, max_max])

        # 调整坐标范围
        self._x_max = max(max(self._x_data), self._x_max)
        self._x_min = min(min(self._x_data), self._x_min)
        self.ax.set_xlim(self._x_min, self._x_max)

        self._y_max = max(max(self._y_data), self._y_max)
        self._y_min = min(min(self._y_data), self._y_min)
        self.ax.set_ylim(self._y_min, self._y_max)

        # 重绘画布
        self.canvas.draw()

    def clear_plot(self):
        """清空图表"""
        self._x_data = []
        self._y_data = []
        self.aline.set_data([], [])
        self.canvas.draw()


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LightStabilityWidget()
    window.show()
    sys.exit(app.exec_())
