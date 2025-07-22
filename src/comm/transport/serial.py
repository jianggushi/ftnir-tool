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
        self._is_running = False

    def open(self):
        if self.is_open:
            logger.warning(f"serial port {self.port} already opened")
            return
        try:
            self._serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=self.bytesize,
                stopbits=self.stopbits,
                parity=self.parity,
            )
            # start the read thread
            self._read_thread = Thread(target=self._receive_loop, daemon=True)
            self._is_running = True
            self._read_thread.start()

            logger.info(f"opened serial port {self.port} successfully")
        except serial.SerialException as e:
            logger.error(f"failed to open serial port {self.port}: {e}")
            self._serial = None
            raise
        except Exception as e:
            logger.error(f"an UNEXPECTED error occurred while opening {self.port}: {e}")
            if self._serial:
                self._serial.close()
                self._serial = None
            self._is_running = False
            raise

    def close(self):
        try:
            self._is_running = False  # 通知接收线程停止
            if self._read_thread and self._read_thread.is_alive():
                self._read_thread.join()  # 等待读取线程安全退出
            self._read_thread = None
            if self._serial and self._serial.is_open:
                self._serial.close()
                return
            self._serial = None
            logger.info(f"close serial port {self.port} success")
        except serial.SerialException as e:
            logger.error(f"close serial port {self.port} failed: {e}")

    @property
    def is_open(self) -> bool:
        return self._serial and self._serial.is_open

    def send_data(self, data: bytes):
        # logger.debug(f"Sending data: {data.hex()}")
        if not isinstance(data, bytes) or not data:
            logger.error("send data failed: data must be bytes and not empty")
            return
        if not self._serial.is_open:
            logger.error("send data failed: serial port not opened")
            return
        try:
            for i in range(0, len(data), 2048):
                chunk = data[i : i + 2048]
                n = self._serial.write(chunk)
                if n != len(chunk):
                    logger.warning("send data failed: data length not match")
                self._serial.flush()  # 确保数据被发送
                time.sleep(0.01)  # 确保数据发送间隔
        except serial.SerialTimeoutException:
            logger.error("send data failed: timeout")
            raise
        except serial.SerialException as e:
            logger.error(f"send data failed: serial port error {e}")
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
        while self._is_running:
            try:
                data = self._serial.read(1)  # 阻塞式读取，等待数据到达
                if self._serial.in_waiting > 0:
                    data += self._serial.read(self._serial.in_waiting)
                if data:
                    print(data.hex(sep=" "))
                    self._emit_data(data)
            except serial.SerialException as e:
                logger.error(f"接收失败: 串口错误 {e}")
            except Exception as e:
                logger.error(f"接收失败：{e}")
            time.sleep(0.01)

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
