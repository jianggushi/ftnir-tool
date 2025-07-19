from PySide6.QtWidgets import QApplication, QWidget

import sys

app = QApplication(sys.argv)

# create a Qt widget
window = QWidget()
# show window
window.show()

# start event loop
app.exec()