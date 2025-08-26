import logging
import struct

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager
from core.model.types import HumidityData


from .base import BaseService

logger = logging.getLogger(__name__)


class HumidityService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager

        self.comm_manager.register_handler(Command.HUMIDITY_RES, self)

    def handle(self, msg: RawMessage):
        if msg.command != Command.HUMIDITY_RES:
            return

        humidity = struct.unpack(">f", msg.data)[0]

        self._run_callbacks(HumidityData(humidity, 0))

    def get_humidity(self):
        self.comm_manager.send_message(Command.HUMIDITY_REQ)
