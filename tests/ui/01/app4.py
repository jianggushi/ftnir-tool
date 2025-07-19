from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow

import sys

app = QApplication(sys.argv)

window = QMainWindow()
window.setWindowTitle("My App")

button = QPushButton("Push me")
window.setCentralWidget(button)
# show window
window.show()

# start event loop
app.exec()