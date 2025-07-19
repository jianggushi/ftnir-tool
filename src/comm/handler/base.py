from abc import ABC, abstractmethod
from ..protocol.parser import RawMessage


class MessageHandler(ABC):
    @abstractmethod
    def handle(self, msg: RawMessage):
        """处理特定类型的消息"""
        pass
