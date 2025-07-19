from typing import Generator
import struct
from .command import Command
from .message import RawMessage

START_FLAG = b"\xa5\x5a"
START_FLAG_LEN = len(START_FLAG)

END_FLAG = b"\xfe\xef"
END_FLAG_LEN = len(END_FLAG)

HEADER_LEN = START_FLAG_LEN + 1 + 2
FOOTER_LEN = 2 + END_FLAG_LEN

MIN_MESSAGE_LEN = HEADER_LEN + FOOTER_LEN


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
            start_index = self._buffer.find(START_FLAG)
            if start_index == -1:
                break
            if start_index > 0:
                # 丢弃消息头之前的无效数据
                self._buffer = self._buffer[start_index:]

            if len(self._buffer) < MIN_MESSAGE_LEN:
                # 数据不足，等待更多数据
                break

            command_val, data_len = struct.unpack(
                ">BH", self._buffer[START_FLAG_LEN:HEADER_LEN]
            )

            message_len = MIN_MESSAGE_LEN + data_len
            if len(self._buffer) < message_len:
                # 数据不足，等待更多数据
                break

            message_bytes = self._buffer[:message_len]

            # TODO: CRC
            try:
                command = Command(command_val)
            except ValueError:
                # 未知命令类型
                self._buffer = self._buffer[START_FLAG_LEN]
                continue

            data_bytes = message_bytes[HEADER_LEN:-FOOTER_LEN]
            yield RawMessage(command, data_bytes)

            self._buffer = self._buffer[message_len:]

    @staticmethod
    def pack(command: Command, data: bytes = b"") -> bytes:
        """
        打包消息为字节流
        """
        data_len = len(data)
        crc = 0
        header = START_FLAG + struct.pack(">BH", command.value, data_len)
        footer = struct.pack(">H", crc) + END_FLAG
        return header + data + footer
