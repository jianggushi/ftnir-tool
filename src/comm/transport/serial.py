import serial
import serial.tools.list_ports
import time
import random
import logging
from threading import Thread
import queue
from queue import Queue

from .transport import ITransport

logger = logging.getLogger(__name__)


class SerialTransport(ITransport):

    def __init__(self, port: str = ""):
        super().__init__()
        self.port = port
        self.baudrate = 115200
        self.bytesize = 8
        self.stopbits = 1
        self.parity = "N"

        self._serial: serial.Serial = None

        self._is_running = False
        self._receive_thread: Thread = None
        self._process_thread: Thread = None
        self._process_queue = Queue(maxsize=100)

    def set_port(self, port: str):
        if self.is_open:
            logger.warning(
                f"serial port {self.port} is already opened, cannot change port"
            )
            return
        self.port = port
        logger.info(f"set serial port to {self.port}")

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
                timeout=1,  # 1 second timeout for read operations
            )
            # start the receive and process threads
            self._is_running = True
            self._process_thread = Thread(target=self._process_loop, daemon=True)
            self._receive_thread = Thread(target=self._receive_loop, daemon=True)
            self._process_thread.start()
            self._receive_thread.start()

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
        if not self.is_open and not self._is_running:
            logger.warning(f"serial port {self.port} is already closed")
            return
        try:
            # notify threads to stop
            self._is_running = False

            # close serial port
            if self._serial and self._serial.is_open:
                self._serial.close()

            # wait for receive thread to finish
            if self._receive_thread and self._receive_thread.is_alive():
                self._receive_thread.join(timeout=2)  # 等待读取线程安全退出

            # wait for process thread to finish
            if self._process_thread and self._process_thread.is_alive():
                self._process_thread.join(timeout=2)  # 等待读取线程安全退出

            logger.info(f"closed serial port {self.port} success")
        except serial.SerialException as e:
            logger.error(f"failed to close serial port {self.port}: {e}")
        finally:
            self._serial = None
            self._receive_thread = None
            self._process_thread = None

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
        logger.debug("receive loop started")
        while self._is_running:
            try:
                # block on reading data
                data = self._serial.read(1)
                if not data:
                    continue

                if self._serial.in_waiting > 0:
                    data += self._serial.read(self._serial.in_waiting)
                    # non-blocking put to process queue
                    self._process_queue.put(data, block=False)
            except serial.SerialException as e:
                logger.error(f"failed to read data from serial port: {e}")
            except queue.Full:
                logger.warning("failed to put data to process queue: queue is full")
            except Exception as e:
                logger.error(f"failed to receive data: {e}")
        logger.debug("receive loop finished")

    def _process_loop(self):
        logger.debug("process loop started")
        while self._is_running:
            try:
                data = self._process_queue.get(timeout=1)
                if data:
                    self._emit_data(data)
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"failed to process data: {e}")
        logger.debug("process loop finished")

    def list_ports(self) -> list[str]:
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports
