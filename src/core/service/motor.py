import logging
import struct

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager

from .base import BaseHandler

logger = logging.getLogger(__name__)


class RotateMotorService(BaseHandler):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager

    def handle(self, msg: RawMessage):
        pass

    def set_rotate_offset(self, offset: int):
        self.comm_manager.send_message(
            Command.SET_ROTATE_OFFSET, struct.pack(">H", offset)
        )

    def set_rotate_target(self, target: int):
        self.comm_manager.send_message(
            Command.SET_ROTATE_TARGET, struct.pack(">B", target)
        )


class ScrewMotorService(BaseHandler):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager

    def handle(self, msg: RawMessage):
        pass

    def set_screw_offset(self, offset: int):

        self.comm_manager.send_message(
            Command.SET_SCREW_OFFSET, struct.pack(">H", offset)
        )

    def set_screw_target(self, target: int):
        self.comm_manager.send_message(
            Command.SET_SCREW_TARGET, struct.pack(">B", target)
        )
