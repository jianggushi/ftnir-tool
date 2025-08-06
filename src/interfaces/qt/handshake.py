import struct
import logging
import threading
from typing import Callable

from comm.transport.transport import ITransport
from comm.transport.serial import SerialTransport
from comm.protocol.parser import MessageParser
from comm.protocol.parser import RawMessage
from comm.protocol.parser import Command

from core.service.base import MessageHandler
from core.service.light_stablity import LightStabilityHandler

logger = logging.getLogger(__name__)


class HandshakeControler(MessageHandler):
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
        if msg.command == Command.HANDSHAKE_RES:
            self._handshake_complete = True
            if self._handshake_timer:
                self._handshake_timer.cancel()
                self._handshake_timer = None
        elif msg.command == Command.HANDSHAKE_REQ:
            self._send_message(Command.HANDSHAKE_RES, b"")

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
