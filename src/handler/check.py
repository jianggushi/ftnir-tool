from typing import Callable
from .base import MessageHandler
from comm.protocol.parser import RawMessage, Command
import logging

logger = logging.getLogger(__name__)


class CheckHandler(MessageHandler):
    def __init__(self):
        self._stability_callback = None
        self._accuracy_callback = None
        self._repeatability_callback = None

    def set_stability_callback(self, callback: Callable[[bytes], None]):
        self._stability_callback = callback

    def set_accuracy_callback(self, callback: Callable[[bytes], None]):
        self._accuracy_callback = callback

    def set_repeatability_callback(self, callback: Callable[[bytes], None]):
        self._repeatability_callback = callback

    def handle(self, msg: RawMessage):
        if msg.command == Command.CHECK_RESP:
            check_type = msg.data[0]
            check_data = msg.data[1:]

            try:
                if check_type == 0x01 and self._stability_callback:
                    self._stability_callback(check_data)
                elif check_type == 0x02 and self._accuracy_callback:
                    self._accuracy_callback(check_data)
                elif check_type == 0x03 and self._repeatability_callback:
                    self._repeatability_callback(check_data)
            except Exception as e:
                logger.error(f"处理检查数据失败: {e}")
