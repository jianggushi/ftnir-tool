class MessageType:
    BACKGROUND_SP = 0x10  # 背景光谱
    SAMPLE_SP = 0x11  # 样品光谱


class Message:
    """
    消息结构：
    起始标志（2字节）|消息类型（1字节）|负载长度（4字节）|数据负载（N字节）|校验和（2字节）|结束标志（2字节）
    """

    START_FLAG = b"\xa5\x5a"
    END_FLAG = b"\xfe\xef"
    HEADER_LEN = len(START_FLAG) + 1 + 4
    FOOTER_LEN = 2 + len(END_FLAG)
    MIN_MESSAGE_LEN = HEADER_LEN + FOOTER_LEN

    def __init__(self, message_type: MessageType, payload: bytes):
        self.message_type = message_type
        self.payload = payload
        self.payload_len = len(payload)
        self.checksum = 0

    def serialize(self) -> bytes:
        """
        序列化消息
        """
        pass

    def deserialize(self, data: bytes):
        """
        反序列化消息
        """
        pass

    def __repr__(self):
        pass
