import serial
import time
import random
import logging
from threading import Thread
from .transport import ITransport

logger = logging.getLogger(__name__)


class SerialTransport(ITransport):

    def __init__(self, port: str):
        super().__init__()
        self.port = port
        self.baudrate = 115200
        self.bytesize = 8
        self.stopbits = 1
        self.parity = "N"

        self._serial: serial.Serial = None
        self._read_thread: Thread = None
        self._is_running: bool = False

    def open(self):
        if self._serial and self._serial.is_open:
            logger.warning(f"串口 {self.port} 已经处于打开状态")
            return
        try:
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                stopbits=self.stopbits,
                parity=self.parity,
            )
            self._read_thread = Thread(target=self._receive_loop, daemon=True)
            self._read_thread.start()
            self._is_running = True
            logger.info(f"打开串口 {self.port} 成功")
        except serial.SerialException as e:
            logger.error(f"打开串口 {self.port} 失败: {e}")
            self._serial = None
            raise

    def close(self):
        self._is_running = False
        try:
            if self._read_thread and self._read_thread.is_alive():
                self._read_thread.join()  # 等待读取线程安全退出
            self._read_thread = None
            if self._serial and self._serial.is_open:
                self._serial.close()
                return
            self._serial = None
            logger.info(f"关闭串口 {self.port} 成功")
        except serial.SerialException as e:
            logger.error(f"关闭串口 {self.port} 失败: {e}")

    @property
    def is_open(self) -> bool:
        return self._serial is not None and self._serial.is_open

    def send_data(self, data: bytes):
        if not isinstance(data, bytes) or not data:
            logger.error("发送失败：数据必须为字节类型且不能为空")
            return
        if not self._serial.is_open:
            logger.error("发送失败：串口未打开")
            return
        try:
            n = self._serial.write(data)
            if n != len(data):
                logger.error("发送失败：数据长度与发送长度不一致")
        except serial.SerialTimeoutException:
            logger.error("发送失败：超时")
            raise
        except serial.SerialException as e:
            logger.error(f"发送失败: 串口错误 {e}")
            raise

    def receive_data(self) -> bytes:
        if not self._serial.is_open:
            logger.warning("接收失败：串口未打开")
            return b""
        try:
            if self._serial.in_waiting > 0:
                data = self._serial.read(self._serial.in_waiting)
                return data
        except serial.SerialException as e:
            logger.error(f"接收失败: 串口错误 {e}")
            return b""

        return b""

    def _receive_loop(self):
        print("start receive loop")
        while self._is_running and self._serial:
            try:
                if self._serial.in_waiting > 0:
                    data = self._serial.read(self._serial.in_waiting)
                    self._emit_data(data)
            except serial.SerialException as e:
                logger.error(f"接收失败: 串口错误 {e}")
                self._is_running = False
            except Exception as e:
                logger.error(f"接收失败：{e}")
                self._is_running = False
            time.sleep(0.01)
        if self._serial and self._serial.is_open:
            self._serial.close()

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
