import logging

from comm.transport.serial import SerialTransport
from comm.protocol.parser import Command
from comm.manager import CommManager
from core.service.handshake import HandshakeService
from core.service.light import LightService
from core.service.signal import LightStabilityService
from core.service.motor import RotateMotorService
from core.service.motor import ScrewMotorService
from core.service.hardware import HardwareService
from core.service.collect import CollectService
from ui_qt.main_window import MainWindow

from .communication import CommController
from .light import LightController
from .signal import LightStabilityController
from .motor import RotateMotorController
from .motor import ScrewMotorController
from .hardware import HardwareController
from .collect import CollectController


logger = logging.getLogger(__name__)


class MainController:
    def __init__(self, view: MainWindow):
        self.view = view

        self.transport = SerialTransport()

        self.comm_manager = CommManager(self.transport)

        # 通信控制
        self.handshake_svc = HandshakeService(self.comm_manager)
        self.comm_controller = CommController(
            self.handshake_svc,
            self.view.control_widget.comm_widget,
            self.comm_manager,
            self.view.status_bar,
        )
        self.comm_manager.register_handler(Command.HANDSHAKE_REQ, self.handshake_svc)
        self.comm_manager.register_handler(Command.HANDSHAKE_RES, self.handshake_svc)

        # 光源控制
        self.light_svc = LightService(self.comm_manager)
        self.light_controller = LightController(
            self.light_svc,
            self.view.control_widget.light_widget,
            self.view.status_bar,
        )

        # 旋转电机控制
        self.rotate_motor_svc = RotateMotorService(self.comm_manager)
        self.rotate_motor_controller = RotateMotorController(
            self.rotate_motor_svc,
            self.view.control_widget.rotate_widget,
        )

        # 丝杠电机控制
        self.screw_motor_svc = ScrewMotorService(self.comm_manager)
        self.screw_motor_controller = ScrewMotorController(
            self.screw_motor_svc,
            self.view.control_widget.screw_widget,
        )

        # 硬件控制
        self.hardware_svc = HardwareService(self.comm_manager)
        self.hardware_controller = HardwareController(
            self.hardware_svc,
            self.view.control_widget.hardware_widget,
        )

        # 数据采集
        self.collect_svc = CollectService(self.comm_manager)
        self.collect_controller = CollectController(
            self.collect_svc,
            self.view.control_widget.collect_widget,
            self.view.spectrum_widget,
        )
        self.comm_manager.register_handler(
            Command.COLLECT_DARK_NOISE_RES, self.collect_svc
        )
        self.comm_manager.register_handler(
            Command.COLLECT_BACKGROUND_RES, self.collect_svc
        )
        self.comm_manager.register_handler(Command.COLLECT_SAMPLE_RES, self.collect_svc)

        # 光源稳定性检查
        self.light_stability_svc = LightStabilityService(self.comm_manager)
        self.light_stability_controller = LightStabilityController(
            self.light_stability_svc,
            self.view.light_stability_widget,
        )
        self.comm_manager.register_handler(
            Command.CHECK_LIGHT_STABILITY_RES, self.light_stability_svc
        )
