from model.serial_communicator import SerialModel
from PySide6.QtWidgets import QPushButton


class SerialController:
    def __init__(self, open_button: QPushButton, collect_button: QPushButton):
        self.model = SerialModel()
        self.open_button = open_button
        self.collect_button = collect_button

        self.open_button.clicked.connect(self.open_serial)
        self.collect_button.clicked.connect(self.start_collect)

    def open_serial(self):
        print("open_serial")
        self.model.open_serial()
        self.open_button.setText("串口已打开")

    def start_collect(self):
        self.model.start_collect()
