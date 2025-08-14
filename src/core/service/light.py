import logging

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager

from .base import BaseHandler

logger = logging.getLogger(__name__)


class LightService(BaseHandler):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager

    def handle(self, msg: RawMessage):
        pass

    def turn_on_light(self):
        self.comm_manager.send_message(Command.TURN_ON_LIGHT)

    def turn_off_light(self):
        self.comm_manager.send_message(Command.TURN_OFF_LIGHT)

    def turn_on_laser(self):
        self.comm_manager.send_message(Command.TURN_ON_LASER)

    def turn_off_laser(self):
        self.comm_manager.send_message(Command.TURN_OFF_LASER)
