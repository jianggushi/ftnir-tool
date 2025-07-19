from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button_is_checked = True
        self.setWindowTitle("My App")

        button = QPushButton("Push me")
        button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)
        button.clicked.connect(self.the_button_was_toggled)
        button.setChecked(self.button_is_checked)

        self.setCentralWidget(button)
    
    def the_button_was_clicked(self):
        print("Clicked")
    
    def the_button_was_toggled(self, checked):
        self.button_is_checked = checked
        print("Checked?", self.button_is_checked)

app = QApplication(sys.argv)

window = MainWindow()
# show window
window.show()

# start event loop
app.exec()