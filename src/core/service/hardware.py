import logging
import struct

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager

from .base import BaseService

logger = logging.getLogger(__name__)


class HardwareService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager

    def handle(self, msg: RawMessage):
        pass

    def set_hardware_setting(self, setting: int):
        self.comm_manager.send_message(
            Command.SET_HARDWARE_SETTING, struct.pack(">B", setting)
        )
