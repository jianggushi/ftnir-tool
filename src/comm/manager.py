import logging
import threading

from comm.protocol.parser import RawMessage
from comm.protocol.message import Message
from comm.protocol.command import Command
from comm.transport.serial import ITransport
from comm.protocol.parser import MessageParser
from core.service.base import BaseHandler

logger = logging.getLogger(__name__)


class CommManager:
    def __init__(self, transport: ITransport):
        self.transport = transport
        self.transport.on_data_received(self._handle_raw_data)

        self._lock = threading.Lock()
        self._parser = MessageParser()
        self._message_handlers: dict[Command, BaseHandler] = {}

    def send_message(self, command: Command, data: bytes = b""):
        """发送消息"""
        message_bytes = Message.pack(command, data)
        self.transport.send_data(message_bytes)
        logger.info(f"send message: {command.name}")

    def _handle_raw_data(self, data: bytes):
        """处理接收到的原始数据"""
        with self._lock:
            self._parser.feed(data)
            for raw_message in self._parser.parse():
                self._process_message(raw_message)

    def _process_message(self, msg: RawMessage):
        """处理接收到的消息"""
        logger.info(
            f"received message: {msg.command.name}, payload length: {len(msg.data)}"
        )
        handler = self._message_handlers.get(msg.command)
        if handler:
            handler.handle(msg)
        else:
            logger.warning(f"no handler found for message: {msg.command.name}")

    def register_handler(self, command: Command, handler: BaseHandler):
        """注册消息处理器"""
        self._message_handlers[command] = handler

    def unregister_handler(self, command: Command):
        """注销消息处理器"""
        if command in self._message_handlers:
            del self._message_handlers[command]

    def connect(self, **kwargs):
        self.transport.open(**kwargs)

    def disconnect(self):
        self.transport.close()

    def list_ports(self) -> list[str]:
        """获取可用端口列表"""
        return self.transport.list_ports()
