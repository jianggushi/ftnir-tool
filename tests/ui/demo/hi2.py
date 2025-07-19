import sys
import time
import random
import serial
import serial.tools.list_ports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import rcParams
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QTextEdit, QLineEdit, QLabel, QGridLayout, QGroupBox, QMessageBox,
    QDialog, QDialogButtonBox
)
from PySide6.QtCore import QThread, Signal, Slot, Qt
from PySide6.QtGui import QColor, QPalette, QAction

# 设置matplotlib字体，防止中文乱码
rcParams['font.sans-serif'] = ['SimHei']
rcParams['axes.unicode_minus'] = False

class SerialReadThread(QThread):
    data_received = Signal(bytes)

    def __init__(self, serial_instance, parent=None):
        super().__init__(parent)
        self.serial = serial_instance
        self.is_running = False
        self.buffer = b""

    def run(self):
        self.is_running = True
        while self.is_running and self.serial.is_open:
            try:
                if self.serial.in_waiting > 0:
                    self.buffer += self.serial.read(self.serial.in_waiting)
                    while b"\n" in self.buffer:
                        frame, self.buffer = self.buffer.split(b"\n", 1)
                        if frame:
                            self.data_received.emit(frame)
            except serial.SerialException as e:
                print(f"Serial read error: {e}")
                break
        self.is_running = False

    def stop(self):
        self.is_running = False
        self.quit()
        self.wait()

class SerialWriteThread(QThread):
    def __init__(self, serial_instance, parent=None):
        super().__init__(parent)
        self.serial = serial_instance
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running and self.serial.is_open:
            try:
                numbers = [random.randint(0, 1000) for _ in range(500)]
                data_string = ",".join(map(str, numbers)) + "\n"
                data_to_send = data_string.encode('ascii')
                self.serial.write(data_to_send)
                time.sleep(1)
            except serial.SerialException as e:
                print(f"Serial write error: {e}")
                break
        self.is_running = False

    def stop(self):
        self.is_running = False
        self.quit()
        self.wait()

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
        self.ax.plot(values, linestyle='-', marker='')
        self.ax.set_title("数据折线图")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.draw()

class SerialAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("串口助手（含图表显示）")
        self.setGeometry(100, 100, 1000, 600)

        self.serial = serial.Serial()
        self.serial_read_thread = None
        self.serial_write_thread = None
        self.fixed_port = "COM1"

        self.serial_settings = {
            'baudrate': 115200,
            'bytesize': 8,
            'stopbits': 1,
            'parity': 'N'
        }

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        control_panel_layout = QVBoxLayout()

        self.connect_button = QPushButton(f"打开串口 ({self.fixed_port})")
        self.connect_button.setCheckable(True)
        self.connect_button.clicked.connect(self.toggle_connection)
        control_panel_layout.addWidget(self.connect_button)

        self.status_label = QLabel("状态: 未连接")
        control_panel_layout.addWidget(self.status_label)
        control_panel_layout.addStretch()

        control_widget = QWidget()
        control_widget.setLayout(control_panel_layout)
        control_widget.setFixedWidth(200)

        data_layout = QVBoxLayout()

        self.receive_text = QTextEdit()
        self.receive_text.setReadOnly(True)
        data_layout.addWidget(self.receive_text, 1)

        self.plot_canvas = PlotCanvas(self)
        data_layout.addWidget(self.plot_canvas, 2)

        main_layout.addWidget(control_widget)
        main_layout.addLayout(data_layout)

    @Slot(bool)
    def toggle_connection(self, checked):
        if checked:
            try:
                self.serial.port = self.fixed_port
                self.serial.baudrate = self.serial_settings['baudrate']
                self.serial.bytesize = self.serial_settings['bytesize']
                self.serial.stopbits = self.serial_settings['stopbits']
                self.serial.parity = self.serial_settings['parity']
                self.serial.open()

                self.serial_read_thread = SerialReadThread(self.serial)
                self.serial_read_thread.data_received.connect(self.update_received_data)
                self.serial_read_thread.start()

                self.serial_write_thread = SerialWriteThread(self.serial)
                self.serial_write_thread.start()

                self.status_label.setText("状态: 已连接")
            except serial.SerialException as e:
                QMessageBox.critical(self, "错误", f"无法打开串口: {e}")
                self.connect_button.setChecked(False)
        else:
            if self.serial.is_open:
                if self.serial_read_thread:
                    self.serial_read_thread.stop()
                if self.serial_write_thread:
                    self.serial_write_thread.stop()
                self.serial.close()
            self.status_label.setText("状态: 未连接")

    @Slot(bytes)
    def update_received_data(self, data):
        text = data.decode('utf-8', errors='replace')
        self.receive_text.append(text)
        self.receive_text.verticalScrollBar().setValue(self.receive_text.verticalScrollBar().maximum())

        try:
            values = [int(val) for val in text.strip().split(',') if val.strip().isdigit()]
            if len(values) == 500:
                self.plot_canvas.update_plot(values)
        except Exception as e:
            print(f"绘图数据解析失败: {e}")

    def closeEvent(self, event):
        if self.serial.is_open:
            if self.serial_read_thread:
                self.serial_read_thread.stop()
            if self.serial_write_thread:
                self.serial_write_thread.stop()
            self.serial.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SerialAssistant()
    window.show()
    sys.exit(app.exec())
