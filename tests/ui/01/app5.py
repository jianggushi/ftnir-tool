from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PySide6.QtCore import QSize

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        button = QPushButton("Push me")
        
        self.setFixedSize(QSize(400, 300))
        self.setCentralWidget(button)

app = QApplication(sys.argv)

window = MainWindow()
# show window
window.show()

# start event loop
app.exec()