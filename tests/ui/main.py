import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from myui_ui import Ui_MainWindow

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class MainWindow(QMainWindow):
    def __init__(self, parent = None) :
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.click)

    def click(self):
        self.ui.pushButton.setText("测试")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("第一个程序")
    window.show()
    app.exit(app.exec())
