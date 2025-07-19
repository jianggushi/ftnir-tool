from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self. button = QPushButton("Push me")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)
    
    def the_button_was_clicked(self):
        self.button.setText("You already clicked me")
        self.button.setEnabled(False)
        print("Clicked")
        self.setWindowTitle("My Oneshot App")

app = QApplication(sys.argv)

window = MainWindow()
# show window
window.show()

# start event loop
app.exec()