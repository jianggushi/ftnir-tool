import logging

from PySide6.QtCore import Slot

from comm.transport.serial import SerialTransport
from comm.protocol.parser import Command
from comm.manager import CommManager
from ui_qt.main_window import MainWindow

from core.service.handshake import HandshakeService
from .communication import CommController, ConnectionStatus

from core.service.light import LightService
from .light import LightController

from core.service.signalcheck import (
    LightStabilityService,
    WaveAccuracyService,
    WaveRepeatabilityService,
    LaserStabilityService,
)
from .signalcheck import (
    LightStabilityController,
    WaveAccuracyController,
    WaveRepeatabilityController,
    LaserStabilityController,
)

from core.service.motor import RotateMotorService, ScrewMotorService
from .motor import RotateMotorController, ScrewMotorController

from core.service.hardware import HardwareService
from .hardware import HardwareController

from core.service.collect import CollectService
from .collect import CollectController

from core.service.temperature import TemperatureService
from .temperature import TemperatureController

from core.service.humidity import HumidityService
from .humidity import HumidityController


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
        self.comm_controller.connection_status.connect(self.on_connection_status)

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

        # 波长准确性检查
        self.wave_accuracy_svc = WaveAccuracyService(self.comm_manager)
        self.wave_accuracy_controller = WaveAccuracyController(
            self.wave_accuracy_svc,
            self.view.wave_accuracy_widget,
        )

        # 波长重复性检查
        self.wave_repeatability_svc = WaveRepeatabilityService(self.comm_manager)
        self.wave_repeatability_controller = WaveRepeatabilityController(
            self.wave_repeatability_svc,
            self.view.wave_repeatability_widget,
        )

        # 激光稳定性检查
        self.laser_stability_svc = LaserStabilityService(self.comm_manager)
        self.laser_stability_controller = LaserStabilityController(
            self.laser_stability_svc,
            self.view.laser_stability_widget,
        )

        self.temperature_svc = TemperatureService(self.comm_manager)
        self.temperature_controller = TemperatureController(
            self.temperature_svc,
            None,
            self.view.status_bar,
        )

        self.humidity_svc = HumidityService(self.comm_manager)
        self.humidity_controller = HumidityController(
            self.humidity_svc,
            None,
            self.view.status_bar,
        )

    @Slot(str)
    def on_connection_status(self, status: str):
        if status == ConnectionStatus.CONNECTED.value:
            self.temperature_controller.start_polling()
            self.humidity_controller.start_polling()
