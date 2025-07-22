from dataclasses import dataclass
from .command import Command


@dataclass
class RawMessage:
    command: Command
    data: bytes


class Message:
    """
    消息结构：
    起始标志（2字节）|消息类型（1字节）|消息码（1字节）|负载长度（4字节）|数据负载（N字节）|校验和（2字节）|结束标志（2字节）
    """

    START_FLAG = b"\xa5\x5a"
    START_FLAG_LEN = len(START_FLAG)

    END_FLAG = b"\xfe\xef"
    END_FLAG_LEN = len(END_FLAG)

    HEADER_LEN = START_FLAG_LEN + 2 + 4
    FOOTER_LEN = 2 + END_FLAG_LEN

    MIN_MESSAGE_LEN = HEADER_LEN + FOOTER_LEN

    def __init__(self):
        pass

    # def __init__(self, command: Command, payload: bytes):
    #     self.command = Command
    #     self.payload = payload
    #     self.payload_len = len(payload)
    #     self.checksum = 0

    # @staticmethod
    # def pack(self) -> bytes:
    #     """
    #     序列化消息
    #     """
    #     pass

    # @staticmethod
    # def unpack(self, data: bytes):
    #     """
    #     反序列化消息
    #     """
    #     pass

    # def __repr__(self):
    #     pass
