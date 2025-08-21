import logging
import struct

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager
from core.model.spectrum import TemperatureData


from .base import BaseService

logger = logging.getLogger(__name__)


class TemperatureService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager

        self.comm_manager.register_handler(Command.TEMPERATURE_RES, self)

    def handle(self, msg: RawMessage):
        if msg.command != Command.TEMPERATURE_RES:
            return

        temperature = struct.unpack(">f", msg.data)[0]

        self._run_callbacks(TemperatureData(temperature, 0))

    def get_temperature(self):
        self.comm_manager.send_message(Command.TEMPERATURE_REQ)
