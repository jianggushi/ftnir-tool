import logging
import struct

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager
from config.types import HardwareData

from .base import BaseService

logger = logging.getLogger(__name__)


class PwmService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager

    def handle(self, msg: RawMessage):
        pass

    def set_pwm_param(self, cycle: int, duty: int):
        data_bytes = struct.pack(">IB", cycle, duty)
        self.comm_manager.send_message(Command.SET_PWM_PARAM, data_bytes)
