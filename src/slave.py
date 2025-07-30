import logging
import struct
import time
import sys
import threading
from typing import Callable

from config.log import setup_logging
from util.signal import generate_test_signal
from comm.protocol.command import Command
from comm.transport.serial import SerialTransport
from comm.protocol.parser import MessageParser
from comm.protocol.parser import RawMessage
from comm.protocol.parser import Command

setup_logging()
logger = logging.getLogger(__name__)


class SlaveManager:
    def __init__(self):
        self.transport = SerialTransport("COM2")
        self.transport.on_data_received(self._handle_raw_data)

        self._parser = MessageParser()
        self._lock = threading.Lock()

        self._connected = False

        self._message_handlers: dict[Command, Callable[[RawMessage], None]] = {
            Command.HANDSHAKE_REQ: self.receive_handshake_req,
            Command.CHECK_LIGHT_STABILITY: self.receive_check_light_stability,
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
            handle_func(msg)
        else:
            logger.warning(f"no handler found for message: {msg.command.name}")

    def _send_message(self, command: Command, data: bytes = b""):
        message_bytes = self._parser.pack(command, data)
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
        # 这里可以添加处理逻辑
        t, sig, freq = generate_test_signal()
        test_data = sig.tolist()
        data_bytes = struct.pack(f">{len(test_data)}f", *test_data)
        self._send_message(Command.CHECK_LIGHT_STABILITY_RES, data_bytes)

    def receive_check_stop(self, raw_message: RawMessage):
        """处理停止检测请求"""
        if raw_message.command != Command.CHECK_LIGHT_STABILITY:
            return
        pass


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
