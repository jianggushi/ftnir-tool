import logging

from comm.transport.serial import SerialTransport
from comm.protocol.parser import Command
from comm.manager import CommManager
from core.service.handshake import HandshakeService
from core.service.light import LightService
from core.service.light_stablity import LightStabilityService
from core.service.interference import DarkNoiseHandler
from core.service.interference import BackgroundHandler
from core.service.interference import SampleHandler

from ui_qt.main_window import MainWindow

from .comm_controller import CommController
from .light_controller import LightController
from .light_stability import LightStabilityController


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

        # 光源稳定性检查
        self.light_stability_svc = LightStabilityService(self.comm_manager)
        self.light_stability_controller = LightStabilityController(
            self.light_stability_svc,
            self.view.signal_widget.light_stability_widget,
        )
        self.comm_manager.register_handler(
            Command.CHECK_LIGHT_STABILITY_RES, self.light_stability_svc
        )

        self._connected = False
        # self._handshake = HandshakeControler(self.message_sender)

        self.dark_noise_handler = DarkNoiseHandler()
        self.background_handler = BackgroundHandler()
        self.sample_handler = SampleHandler()

    def connect(self, **kwargs):
        try:
            if not self.transport.is_open:
                port = kwargs.get("port", "")
                self.transport.set_port(port)
                self.transport.open()
                self._connected = True
                self.status_bar_updated.emit("transport", "已打开")

            # 开始握手
            self._handshake.start()
        except Exception as e:
            logger.error(f"连接失败: {e}")
            self.status_bar_updated.emit("transport", "错误")
            self.disconnect()

    def disconnect(self):
        self._connected = False
        self._handshake.stop()
        logger.info("stoped handshake")
        if self.transport.is_open:
            self.transport.close()
            self.status_bar_updated.emit("transport", "关闭")

    def list_ports(self) -> list[str]:
        return self.transport.list_ports()

    @property
    def is_connected(self) -> bool:
        return self._connected
