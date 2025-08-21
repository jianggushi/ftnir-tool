import logging
import struct
from typing import Callable
from abc import ABC, abstractmethod

from comm.protocol.parser import RawMessage

logger = logging.getLogger(__name__)


class BaseService(ABC):
    def __init__(self):
        self._callbacks: list[Callable[[object], None]] = []

    def add_callback(self, callback: Callable[[object], None]):
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[object], None]):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def clear_callbacks(self):
        self._callbacks.clear()

    def _run_callbacks(self, data: object = None):
        for callback in self._callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"failed to run callback {callback.__name__}: {e}")

    @abstractmethod
    def handle(self, msg: RawMessage):
        """处理特定类型的消息"""
        pass


def parse_interference_data(data: bytes) -> list[float]:
    """解析干涉数据,每个数据点是4字节浮点数"""
    if len(data) % 4 != 0:
        raise ValueError(f"data length must be a multiple of 4, got {len(data)} bytes")

    count = len(data) // 4
    return list(struct.unpack(f">{count}f", data))
