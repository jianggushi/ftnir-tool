import logging

from comm.protocol.message import Message
from comm.protocol.command import Command
from comm.transport.serial import SerialTransport

logger = logging.getLogger(__name__)


class MessageSender:
    def __init__(self, transport: SerialTransport):
        self.transport = transport

    def send_message(self, command: Command, data: bytes = b""):
        message_bytes = Message.pack(command, data)
        self.transport.send_data(message_bytes)
        logger.info(f"send message: {command.name}")
