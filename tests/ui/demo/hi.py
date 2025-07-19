import sys
import time
import random
import serial
import serial.tools.list_ports
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QComboBox, QPushButton, QTextEdit, QLineEdit, QLabel, QGridLayout, QGroupBox, QMessageBox,
    QDialog, QDialogButtonBox
)
from PySide6.QtCore import QThread, Signal, Slot, Qt
from PySide6.QtGui import QColor, QPalette, QAction

# --- 串口设置对话框 ---
class SettingsDialog(QDialog):
    """
    A dialog window for configuring advanced serial port settings.
    """
    def __init__(self, current_settings, parent=None):
        super().__init__(parent)
        self.setWindowTitle("串口参数配置 (Serial Port Configuration)")
        
        self.settings = current_settings
        
        layout = QVBoxLayout(self)
        form_layout = QGridLayout()

        # Baud Rate
        form_layout.addWidget(QLabel("波特率 (Baud):"), 0, 0)
        self.baud_rate_combo = QComboBox()
        self.baud_rate_combo.addItems(['9600', '19200', '38400', '57600', '115200', '230400', '460800', '921600'])
        self.baud_rate_combo.setCurrentText(str(self.settings['baudrate']))
        form_layout.addWidget(self.baud_rate_combo, 0, 1)

        # Data Bits
        form_layout.addWidget(QLabel("数据位 (Data):"), 1, 0)
        self.data_bits_combo = QComboBox()
        self.data_bits_combo.addItems(['8', '7', '6', '5'])
        self.data_bits_combo.setCurrentText(str(self.settings['bytesize']))
        form_layout.addWidget(self.data_bits_combo, 1, 1)

        # Stop Bits
        form_layout.addWidget(QLabel("停止位 (Stop):"), 2, 0)
        self.stop_bits_combo = QComboBox()
        self.stop_bits_combo.addItems(['1', '1.5', '2'])
        self.stop_bits_combo.setCurrentText(str(self.settings['stopbits']))
        form_layout.addWidget(self.stop_bits_combo, 2, 1)

        # Parity
        parity_map_rev = {'N': 'None', 'E': 'Even', 'O': 'Odd', 'M': 'Mark', 'S': 'Space'}
        form_layout.addWidget(QLabel("校验位 (Parity):"), 3, 0)
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(['None', 'Even', 'Odd', 'Mark', 'Space'])
        self.parity_combo.setCurrentText(parity_map_rev[self.settings['parity']])
        form_layout.addWidget(self.parity_combo, 3, 1)

        layout.addLayout(form_layout)

        # OK and Cancel buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_settings(self):
        """Returns the selected settings as a dictionary."""
        parity_map = {'None': 'N', 'Even': 'E', 'Odd': 'O', 'Mark': 'M', 'Space': 'S'}
        return {
            'baudrate': int(self.baud_rate_combo.currentText()),
            'bytesize': int(self.data_bits_combo.currentText()),
            'stopbits': float(self.stop_bits_combo.currentText()),
            'parity': parity_map[self.parity_combo.currentText()]
        }

# --- 串口读取线程 ---
class SerialReadThread(QThread):
    data_received = Signal(bytes)

    def __init__(self, serial_instance, parent=None):
        super().__init__(parent)
        self.serial = serial_instance
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running and self.serial.is_open:
            try:
                if self.serial.in_waiting > 0:
                    data = self.serial.read(self.serial.in_waiting)
                    self.data_received.emit(data)
            except serial.SerialException as e:
                print(f"Serial read error: {e}")
                break
        self.is_running = False

    def stop(self):
        self.is_running = False
        self.quit()
        self.wait()

# --- 串口自动发送线程 ---
class SerialWriteThread(QThread):
    """
    A thread that automatically sends data every second.
    """
    def __init__(self, serial_instance, parent=None):
        super().__init__(parent)
        self.serial = serial_instance
        self.is_running = False

    def run(self):
        self.is_running = True
        print("Starting writer thread...")
        while self.is_running and self.serial.is_open:
            try:
                # 1. 生成500个0-1000的随机数
                numbers = [random.randint(0, 1000) for _ in range(500)]
                # 2. 格式化为逗号分隔的字符串，并以换行符结尾
                data_string = ",".join(map(str, numbers)) + "\n"
                # 3. 编码为字节串以便发送
                data_to_send = data_string.encode('ascii')

                # 4. 写入串口
                self.serial.write(data_to_send)
                print(f"Writer thread sent a frame of {len(data_to_send)} bytes.")

                # 5. 等待1秒
                time.sleep(1)
            except serial.SerialException as e:
                print(f"Serial write error: {e}")
                break  # On error, stop the thread
        print("Writer thread stopped.")
        self.is_running = False

    def stop(self):
        self.is_running = False
        self.quit()
        self.wait()

# --- 主窗口 ---
class SerialAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 & PySerial 上位机助手 (自动发送模式)")
        self.setGeometry(100, 100, 850, 600)

        self.serial = serial.Serial()
        self.serial_read_thread = None
        self.serial_write_thread = None
        self.fixed_port = "COM1"

        # Store settings in a dictionary for easier management
        self.serial_settings = {
            'baudrate': 115200,
            'bytesize': 8,
            'stopbits': 1,
            'parity': 'N'
        }

        self.init_ui()

    def init_ui(self):
        # --- Create Menu Bar ---
        menu_bar = self.menuBar()
        settings_menu = menu_bar.addMenu("设置 (&Settings)")
        
        configure_action = QAction("串口参数配置... (Configure Serial...)", self)
        configure_action.triggered.connect(self.open_settings_dialog)
        settings_menu.addAction(configure_action)
        
        # --- Main Widget and Layout ---
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # --- Left Panel: Control Panel ---
        control_panel_layout = QVBoxLayout()
        control_panel_layout.setSpacing(10)
        
        # Connection Control
        self.connect_button = QPushButton(f"打开串口 ({self.fixed_port})")
        self.connect_button.setCheckable(True)
        self.connect_button.clicked.connect(self.toggle_connection)
        control_panel_layout.addWidget(self.connect_button)
        
        self.status_label = QLabel("状态: 未连接 (Status: Disconnected)")
        self.status_label.setAlignment(Qt.AlignCenter)
        palette = self.status_label.palette()
        palette.setColor(QPalette.WindowText, QColor('red'))
        self.status_label.setPalette(palette)
        control_panel_layout.addWidget(self.status_label)
        
        control_panel_layout.addStretch()

        # --- Right Panel: Data Display ---
        data_layout = QVBoxLayout()
        
        receive_group = QGroupBox("接收区 (Receive Area)")
        receive_v_layout = QVBoxLayout()
        self.receive_text = QTextEdit()
        self.receive_text.setReadOnly(True)
        receive_v_layout.addWidget(self.receive_text)
        receive_h_layout = QHBoxLayout()
        self.clear_receive_button = QPushButton("清空接收 (Clear)")
        self.clear_receive_button.clicked.connect(lambda: self.receive_text.clear())
        self.receive_format_combo = QComboBox()
        self.receive_format_combo.addItems(["ASCII", "HEX"])
        receive_h_layout.addWidget(self.clear_receive_button)
        receive_h_layout.addStretch()
        receive_h_layout.addWidget(QLabel("接收格式 (Format):"))
        receive_h_layout.addWidget(self.receive_format_combo)
        receive_v_layout.addLayout(receive_h_layout)
        receive_group.setLayout(receive_v_layout)

        data_layout.addWidget(receive_group)

        # --- Combine Left and Right Panels ---
        control_widget = QWidget()
        control_widget.setLayout(control_panel_layout)
        control_widget.setFixedWidth(250)
        
        main_layout.addWidget(control_widget)
        main_layout.addLayout(data_layout)

    def open_settings_dialog(self):
        """Opens the serial port configuration dialog."""
        dialog = SettingsDialog(self.serial_settings, self)
        if dialog.exec():  # exec() shows the dialog modally
            self.serial_settings = dialog.get_settings()
            print("Serial settings updated:", self.serial_settings)

    @Slot(bool)
    def toggle_connection(self, checked):
        if checked:
            try:
                # Use the fixed port name
                self.serial.port = self.fixed_port
                
                # Apply settings from the stored dictionary
                self.serial.baudrate = self.serial_settings['baudrate']
                self.serial.bytesize = self.serial_settings['bytesize']
                self.serial.stopbits = self.serial_settings['stopbits']
                self.serial.parity = self.serial_settings['parity']
                
                self.serial.open()
                
                # Start reader thread
                self.serial_read_thread = SerialReadThread(self.serial)
                self.serial_read_thread.data_received.connect(self.update_received_data)
                self.serial_read_thread.start()

                # Start writer thread
                self.serial_write_thread = SerialWriteThread(self.serial)
                self.serial_write_thread.start()

                self.connect_button.setText(f"关闭串口 ({self.fixed_port})")
                self.status_label.setText(f"状态: 已连接到 {self.serial.port}\n(Status: Connected to {self.serial.port})")
                palette = self.status_label.palette()
                palette.setColor(QPalette.WindowText, QColor('green'))
                self.status_label.setPalette(palette)
                print(f"Successfully opened port {self.serial.port} with settings: {self.serial_settings}")

            except serial.SerialException as e:
                QMessageBox.critical(self, "错误 (Error)", f"无法打开串口 (Could not open port):\n{e}")
                self.connect_button.setChecked(False)
                self.status_label.setText("状态: 打开失败 (Status: Failed to open)")
                palette = self.status_label.palette()
                palette.setColor(QPalette.WindowText, QColor('red'))
                self.status_label.setPalette(palette)
                print(f"Failed to open port: {e}")
        else:
            if self.serial.is_open:
                if self.serial_read_thread:
                    self.serial_read_thread.stop()
                    self.serial_read_thread = None
                if self.serial_write_thread:
                    self.serial_write_thread.stop()
                    self.serial_write_thread = None
                self.serial.close()
                print("Serial port closed.")

            self.connect_button.setText(f"打开串口 ({self.fixed_port})")
            self.status_label.setText("状态: 未连接 (Status: Disconnected)")
            palette = self.status_label.palette()
            palette.setColor(QPalette.WindowText, QColor('red'))
            self.status_label.setPalette(palette)

    @Slot(bytes)
    def update_received_data(self, data):
        if self.receive_format_combo.currentText() == "ASCII":
            text = data.decode('utf-8', errors='replace')
        else: # HEX
            text = data.hex(' ').upper() + ' '
        
        self.receive_text.insertPlainText(text)
        self.receive_text.verticalScrollBar().setValue(self.receive_text.verticalScrollBar().maximum())

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
