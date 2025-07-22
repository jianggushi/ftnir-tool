from typing import Generator
import struct
from .command import Command
from .message import RawMessage, Message


class MessageParser:
    def __init__(self):
        self._buffer = bytearray()

    def feed(self, data: bytes):
        self._buffer.extend(data)

    def parse(self) -> Generator[RawMessage, None, None]:
        """
        从缓冲区中解析出一个完整的消息
        """
        while True:
            start_index = self._buffer.find(Message.START_FLAG)
            if start_index == -1:
                break
            if start_index > 0:
                # 丢弃消息头之前的无效数据
                self._buffer = self._buffer[start_index:]

            if len(self._buffer) < Message.MIN_MESSAGE_LEN:
                # 数据不足，等待更多数据
                break

            command_val, data_len = struct.unpack(
                ">HI", self._buffer[Message.START_FLAG_LEN : Message.HEADER_LEN]
            )

            message_len = Message.MIN_MESSAGE_LEN + data_len
            if len(self._buffer) < message_len:
                # 数据不足，等待更多数据
                break

            message_bytes = self._buffer[:message_len]

            # TODO: CRC
            try:
                command = Command(command_val)
            except ValueError:
                # 未知命令类型
                self._buffer = self._buffer[Message.START_FLAG_LEN]
                continue

            data_bytes = message_bytes[Message.HEADER_LEN : -Message.FOOTER_LEN]
            yield RawMessage(command, data_bytes)

            self._buffer = self._buffer[message_len:]

    @staticmethod
    def pack(command: Command, data: bytes = b"") -> bytes:
        """
        打包消息为字节流
        """
        data_len = len(data)
        crc = 0
        header = Message.START_FLAG + struct.pack(">HI", command.value, data_len)
        footer = struct.pack(">H", crc) + Message.END_FLAG
        return header + data + footer
