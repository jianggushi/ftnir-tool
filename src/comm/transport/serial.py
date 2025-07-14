import serial
import time
import random
import logging
from threading import Thread
from .transport import ITransport


class SerialTransport(ITransport):

    def __init__(self, port: str):
        super().__init__()
        self.port = port
        self.baudrate = 115200
        self.bytesize = 8
        self.stopbits = 1
        self.parity = "N"
        self.serial = serial.Serial()

        # self.read_thread.data_received.connect(self.data_received)

    def connect(self) -> bool:
        if self.serial.is_open:
            logging.warning(f"串口 {self.port} 已经处于打开状态")
            return True

        self.serial.port = self.port
        self.serial.baudrate = self.baudrate
        self.serial.bytesize = self.bytesize
        self.serial.stopbits = self.stopbits
        self.serial.parity = self.parity

        try:
            self.serial.open()
            self._connected = True
        except serial.SerialException as e:
            logging.error(f"打开串口 {self.serial.port} 失败: {e}")
            return False

        logging.debug(f"打开串口 {self.serial.port} 成功")
        return True

    def disconnect(self) -> bool:
        try:
            if self.serial.is_open:
                self.serial.close()
            self._connected = False
        except serial.SerialException as e:
            logging.error(f"关闭串口 {self.serial.port} 失败: {e}")
            return False
        logging.debug(f"关闭串口 {self.serial.port} 成功")
        return True

    def send_data(self, data: bytes) -> bool:
        if not isinstance(data, bytes) or not data:
            logging.error("发送失败：数据必须为字节类型且不能为空")
            return False
        if not self.serial.is_open:
            logging.error("发送失败：串口未打开")
            return False
        try:
            n = self.serial.write(data)
            if n != len(data):
                logging.error("发送失败：数据长度与发送长度不一致")
                return False
        except serial.SerialTimeoutException:
            logging.error("发送失败：超时")
            return False
        except serial.SerialException as e:
            logging.error(f"发送失败: 串口错误 {e}")
            return False
        return True

    def receive_data(self) -> bytes | None:
        if not self.serial.is_open:
            logging.warning("接收失败：串口未打开")
            return None
        try:
            if self.serial.in_waiting > 0:
                data = self.serial.read(self.serial.in_waiting)
                logging.debug(f"读取数据: {data}")
                return data
        except serial.SerialException as e:
            logging.error(f"接收失败: 串口错误 {e}")
            return None

        return None

    def _receive_loop(self):
        while self.serial.is_open:
            try:
                if self.serial.in_waiting > 0:
                    data = self.serial.read(self.serial.in_waiting)
                    if data:
                        self._emit_data(data)
            except Exception as e:
                print(f"Error in receive loop: {e}")
                self._connected = False
            time.sleep(0.01)  # 避免 CPU 占用过高

    def list_ports(self) -> list[str]:
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports


class _ReadThread(Thread):

    def __init__(self, ser: serial.Serial):
        super().__init__(daemon=True)
        self.serial: serial.Serial = ser
        self.is_running: bool = False
        self.buffer: bytes = b""
        # self.callback: callable([bytes], None) = callback

    def run(self):
        self.is_running = True
        while self.is_running and self.serial.is_open:
            if self.serial.in_waiting > 0:
                data = self.serial.read(500 * 2)
                # 将二进制数据解析回整数列表
                nums = [
                    int.from_bytes(data[i : i + 2], "big")
                    for i in range(0, len(data), 2)
                ]
                # while b"\n" in self.buffer:
                #     frame, self.buffer = self.buffer.split(b"\n", 1)
                #     if frame:
                #         self.data_received.emit(frame)
                print(nums)
        self.is_running = False

    def stop(self):
        self.is_running = False
        if self.is_alive():
            self.join()


class _WriteThread(Thread):
    def __init__(self, serial_instance: serial.Serial):
        super().__init__(daemon=True)
        self.serial = serial_instance
        self.is_running = False

    def run(self):
        self.is_running = True
        while self.is_running and self.serial.is_open:
            nums = [random.randint(0, 1000) for _ in range(500)]
            # 转换为HEX格式：每个数字用2字节大端表示，0填充
            hex_data = b"".join([num.to_bytes(2, "big") for num in nums])
            data = hex_data
            # 发送数据
            self.serial.write(data)
            time.sleep(1)
        self.is_running = False

    def stop(self):
        self.is_running = False
        if self.is_alive():
            self.join()  # 等待线程结束
