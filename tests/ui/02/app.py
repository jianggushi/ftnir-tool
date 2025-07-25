from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        button = QPushButton("Push me")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(button)
    
    def the_button_was_clicked(self):
        print("Clicked")

app = QApplication(sys.argv)

window = MainWindow()
# show window
window.show()

# start event loop
app.exec()