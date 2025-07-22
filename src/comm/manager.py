from .transport.transport import ITransport
from .transport.serial import SerialTransport
from .protocol.parser import MessageParser
from .protocol.parser import RawMessage
from .protocol.parser import Command
import threading
import logging
import time
from typing import Callable
from .handler.base import MessageHandler

logger = logging.getLogger(__name__)


class HandshakeManager(MessageHandler):
    def __init__(self, send_message_callback: Callable[[Command, bytes], None]):
        self._send_message = send_message_callback

        self._handshake_complete = False
        self._handshake_timer = None
        self._retry_count = 0

    def start(self):
        """开始握手过程"""
        if self._handshake_complete:
            return

        self._retry_count = 0
        self._start_handshake()

    def stop(self):
        """停止握手过程"""
        self._handshake_complete = False
        if self._handshake_timer:
            self._handshake_timer.cancel()
            self._handshake_timer = None

    def handle(self, msg: RawMessage):
        """处理握手响应"""
        if msg.command == Command.HANDSHAKE_RESP:
            self._handshake_complete = True
            if self._handshake_timer:
                self._handshake_timer.cancel()
                self._handshake_timer = None
        elif msg.command == Command.HANDSHAKE_REQ:
            self._send_message(Command.HANDSHAKE_RESP, b"")

    def _start_handshake(self):
        if self._handshake_complete:
            return

        # 清除之前的定时器
        if self._handshake_timer:
            self._handshake_timer.cancel()
        # 发送握手命令
        self._send_message(Command.HANDSHAKE_REQ, b"")
        # 启动握手超时检查定时器
        self._handshake_timer = threading.Timer(3.0, self._handle_timeout)
        self._handshake_timer.start()

    def _handle_timeout(self):
        """处理握手超时"""
        if not self._handshake_complete:
            self._retry_count += 1
            logging.warning(
                f"Handshake timeout, 5 seconds later will retry {self._retry_count + 1} times..."
            )
            # 5秒后重试
            self._handshake_timer = threading.Timer(5.0, self._start_handshake)
            self._handshake_timer.start()


class CommManager:
    def __init__(self, serial_port: str = "COM1"):
        self.transport = SerialTransport(serial_port)
        self.transport.on_data_received(self._handle_raw_data)

        self._parser = MessageParser()
        self._lock = threading.Lock()

        self._connected = False
        self._handshake = HandshakeManager(self._send_message)

        self._message_handlers: dict[Command, MessageHandler] = {
            Command.HANDSHAKE_REQ: self._handshake,
            Command.HANDSHAKE_RESP: self._handshake,
        }

    def connect(self):
        try:
            if not self.transport.is_open:
                self.transport.open()
                self._connected = True
            # 开始握手
            self._handshake.start()
        except Exception as e:
            logger.error(f"连接失败: {e}")
            self.disconnect()

    def disconnect(self):
        self._connected = False
        self._handshake.stop()

        if self.transport.is_open:
            self.transport.close()

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _handle_raw_data(self, data: bytes):
        with self._lock:
            self._parser.feed(data)
            for raw_message in self._parser.parse():
                self._process_message(raw_message)

    def _process_message(self, msg: RawMessage):
        """处理接收到的消息"""
        logger.info(f"Received message: {msg.command.name}, Data: {msg.data}")
        handler = self._message_handlers.get(msg.command)
        if handler:
            handler.handle(msg)
        else:
            logger.warning(f"未找到处理器处理命令: {msg.command}")
        # if msg.command == Command.HANDSHAKE:
        #     self._handshake.handle_response()

    def _send_message(self, command: Command, data: bytes = b""):
        message_bytes = self._parser.pack(command, data)
        self.transport.send_data(message_bytes)
        logger.info(f"send message: {command.name}")

    def register_handler(self, command: Command, handler: MessageHandler):
        """注册消息处理器"""
        self._message_handlers[command] = handler

    def unregister_handler(self, command: Command):
        """注销消息处理器"""
        if command in self._message_handlers:
            del self._message_handlers[command]

    def start_collect(self):
        self._send_message(Command.START_COLLECT)

    def stop_collect(self):
        self._send_message(Command.STOP_COLLECT)

    def start_check_stability(self):
        self._send_message(Command.START_CHECK, b"\01")

    def stop_check_stability(self):
        self._send_message(Command.STOP_CHECK, b"\01")

    def start_check_accuracy(self):
        self._send_message(Command.START_CHECK, b"\02")

    def stop_check_accuracy(self):
        self._send_message(Command.STOP_CHECK, b"\02")

    def start_check_repeatability(self):
        self._send_message(Command.START_CHECK, b"\03")

    def stop_check_repeatability(self):
        self._send_message(Command.STOP_CHECK, b"\03")
