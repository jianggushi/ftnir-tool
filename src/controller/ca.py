import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax.set_title("数据折线图")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.data = []

    def update_plot(self, values):
        self.ax.clear()
        self.ax.plot(values, linestyle="-", marker="")
        self.ax.set_title("数据折线图")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.draw()
