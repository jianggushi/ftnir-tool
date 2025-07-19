from PySide6.QtWidgets import QApplication, QWidget, QPushButton

import sys

app = QApplication(sys.argv)

window = QPushButton("Push me")
# show window
window.show()

# start event loop
app.exec()