import logging
import struct
import time
import sys
import random
import threading
from typing import Callable

from config.log import setup_logging
from util.interferogram import generate_test_signal
from util.interferogram_insa import simulate_sample_interferogram
from comm.protocol.command import Command
from comm.transport.serial import SerialTransport
from comm.protocol.parser import MessageParser
from comm.protocol.parser import RawMessage
from comm.protocol.parser import Command
from comm.protocol.message import Message

setup_logging()
logger = logging.getLogger(__name__)


class SlaveManager:
    def __init__(self):
        self.transport = SerialTransport("COM2")
        self.transport.on_data_received(self._handle_raw_data)

        self._parser = MessageParser()
        self._lock = threading.Lock()

        self._connected = False

        self.check_light_stability_running = False
        self.collect_running = False

        self._message_handlers: dict[Command, Callable[[RawMessage], None]] = {
            Command.HANDSHAKE_REQ: self.receive_handshake_req,
            Command.CHECK_LIGHT_STABILITY: self.receive_check_light_stability,
            Command.CHECK_STOP: self.receive_check_stop,
            Command.COLLECT_DARK_NOISE_REQ: self.receive_collect_dark_noise,
            Command.COLLECT_BACKGROUND_REQ: self.receive_collect_background,
            Command.COLLECT_SAMPLE_REQ: self.receive_collect_sample,
            Command.COLLECT_STOP_REQ: self.receive_collect_stop,
            Command.TEMPERATURE_REQ: self.receive_temperature_req,
            Command.HUMIDITY_REQ: self.receive_humidity_req,
        }

    def connect(self):
        try:
            if not self.transport.is_open:
                self.transport.open()
                self._connected = True
        except Exception as e:
            logger.error(f"连接失败: {e}")
            self.disconnect()

    def disconnect(self):
        self._connected = False
        if self.transport.is_open:
            self.transport.close()

    def list_ports(self) -> list[str]:
        return self.transport.list_ports()

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _handle_raw_data(self, data: bytes):
        with self._lock:
            self._parser.feed(data)
            for raw_message in self._parser.parse():
                self._handle_message(raw_message)

    def _handle_message(self, msg: RawMessage):
        """处理接收到的消息"""
        logger.info(
            f"received message: {msg.command.name}, payload length: {len(msg.data)}"
        )
        handle_func = self._message_handlers.get(msg.command)
        if handle_func:
            threading.Thread(target=handle_func, args=(msg,)).start()
        else:
            logger.warning(
                f"no handler found for message: {msg.command.name}, {msg.data}"
            )

    def _send_message(self, command: Command, data: bytes = b""):
        message_bytes = Message.pack(command, data)
        self.transport.send_data(message_bytes)
        logger.info(f"send message: {command.name}")

    def receive_handshake_req(self, raw_message: RawMessage):
        """处理握手请求"""
        if raw_message.command != Command.HANDSHAKE_REQ:
            return
        self._send_message(Command.HANDSHAKE_RES, b"")

    def receive_check_light_stability(self, raw_message: RawMessage):
        """处理光源稳定性检测请求"""
        if raw_message.command != Command.CHECK_LIGHT_STABILITY:
            return

        self.check_light_stability_running = True

        while self.check_light_stability_running:
            t, sig, freq = generate_test_signal()
            test_data = sig.tolist()
            data_bytes = struct.pack(f">{len(test_data)}f", *test_data)
            self._send_message(Command.CHECK_LIGHT_STABILITY_RES, data_bytes)
            time.sleep(0.1)

    def receive_check_stop(self, raw_message: RawMessage):
        """处理停止检测请求"""
        if raw_message.command != Command.CHECK_STOP:
            return
        self.check_light_stability_running = False

    def receive_collect_dark_noise(self, raw_message: RawMessage):
        """处理采集暗噪声请求"""
        if raw_message.command != Command.COLLECT_DARK_NOISE_REQ:
            return
        # 解析请求参数
        num = 0
        continuous_mode = raw_message.data[0] == 0xFF
        if not continuous_mode:
            num = struct.unpack(">H", raw_message.data[1:])[0]

        self.collect_running = True

        while self.collect_running and (num > 0 or continuous_mode):
            t, sig, freq = generate_test_signal()
            test_data = sig.tolist()
            data_bytes = struct.pack(f">{len(test_data)}f", *test_data)
            self._send_message(Command.COLLECT_DARK_NOISE_RES, data_bytes)

            if not continuous_mode:
                num -= 1
            time.sleep(0.1)

    def receive_collect_background(self, raw_message: RawMessage):
        """处理采集背景请求"""
        if raw_message.command != Command.COLLECT_BACKGROUND_REQ:
            return
        # 解析请求参数
        num = 0
        continuous_mode = raw_message.data[0] == 0xFF
        if not continuous_mode:
            num = struct.unpack(">H", raw_message.data[1:])[0]

        self.collect_running = True

        while self.collect_running and (num > 0 or continuous_mode):
            t, sig, freq = generate_test_signal()
            test_data = sig.tolist()
            data_bytes = struct.pack(f">{len(test_data)}f", *test_data)
            self._send_message(Command.COLLECT_BACKGROUND_RES, data_bytes)

            if not continuous_mode:
                num -= 1
            time.sleep(0.1)

    def receive_collect_sample(self, raw_message: RawMessage):
        """处理采集样本请求"""
        if raw_message.command != Command.COLLECT_SAMPLE_REQ:
            return
        # 解析请求参数
        num = 0
        continuous_mode = raw_message.data[0] == 0xFF
        if not continuous_mode:
            num = struct.unpack(">H", raw_message.data[1:])[0]

        self.collect_running = True

        while self.collect_running and (num > 0 or continuous_mode):
            t, sig = simulate_sample_interferogram(
                "../data/insa/001 _2_20250306T103419.txt"
            )

            test_data = sig.tolist()
            data_bytes = struct.pack(f">{len(test_data)}f", *test_data)
            self._send_message(Command.COLLECT_SAMPLE_RES, data_bytes)

            if not continuous_mode:
                num -= 1
            time.sleep(0.1)

    def receive_collect_stop(self, raw_message: RawMessage):
        """处理采集停止请求"""
        if raw_message.command != Command.COLLECT_STOP_REQ:
            return
        self.collect_running = False

    def receive_temperature_req(self, raw_message: RawMessage):
        """处理温度请求"""
        if raw_message.command != Command.TEMPERATURE_REQ:
            return
        # 随机20-30度
        temperature = random.uniform(20.0, 30.0)
        data = struct.pack(">f", temperature)
        self._send_message(Command.TEMPERATURE_RES, data)

    def receive_humidity_req(self, raw_message: RawMessage):
        """处理湿度请求"""
        if raw_message.command != Command.HUMIDITY_REQ:
            return
        # 随机20-30度
        humidity = random.uniform(60.0, 90.0)
        data = struct.pack(">f", humidity)
        self._send_message(Command.HUMIDITY_RES, data)


def run():
    logger.info("Starting Slave Manager...")
    print("Commands: connect, disconnect, exit")
    manager = SlaveManager()
    while True:
        cmd = input("> ").strip().lower()

        if cmd == "connect":
            manager.connect()
        elif cmd == "disconnect":
            manager.disconnect()
        elif cmd == "exit":
            break
        else:
            print("未知命令")
    sys.exit(0)


if __name__ == "__main__":
    run()
