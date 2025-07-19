from abc import ABC, abstractmethod
from typing import Callable
import logging

logger = logging.getLogger(__name__)


class ITransport(ABC):
    def __init__(self):
        self._data_received_callback: Callable[[bytes], None] = None

    @abstractmethod
    def open(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def send_data(self, data: bytes):
        raise NotImplementedError

    @abstractmethod
    def receive_data(self) -> bytes:
        raise NotImplementedError

    @property
    @abstractmethod
    def is_open(self) -> bool:
        raise NotImplementedError

    def on_data_received(self, callback: Callable[[bytes], None]):
        self._data_received_callback = callback

    def _emit_data(self, data: bytes):
        logger.info(data)
        try:
            if self._data_received_callback:
                self._data_received_callback(data)
        except Exception as e:
            logger.error(f"Error in data received callback: {e}")
