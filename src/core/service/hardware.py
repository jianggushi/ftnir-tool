import logging
import struct

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager
from core.model.spectrum import HardwareData

from .base import BaseService

logger = logging.getLogger(__name__)


class HardwareService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager

    def handle(self, msg: RawMessage):
        pass

    def set_hardware_setting(self, data: HardwareData):
        data_bytes = struct.pack(
            ">BBBB", data.resolution, data.velocity, data.direction, data.scan_mode
        )
        self.comm_manager.send_message(Command.SET_HARDWARE_SETTING, data_bytes)
