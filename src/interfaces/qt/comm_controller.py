import logging

from PySide6.QtCore import Slot, QObject, Signal

from comm.manager import CommManager
from core.service.handshake import HandshakeService
from ui_qt.control_widget import CommunicationWidget
from ui_qt.status_bar import StatusBarWidget

logger = logging.getLogger(__name__)


class CommController(QObject):
    connection_status = Signal(str)

    def __init__(
        self,
        svc: HandshakeService,
        view: CommunicationWidget,
        comm_manager: CommManager,
        status_bar: StatusBarWidget,
    ):
        super().__init__()

        self.svc = svc
        self.view = view
        self.comm_manager = comm_manager

        self.connection_status.connect(status_bar.update_transport_label)

        self.view.connect_btn.clicked.connect(self.on_connect)
        self.view.disconnect_btn.clicked.connect(self.on_disconnect)
        self.view.refresh_button.clicked.connect(self.on_refresh_ports)

    def on_connect(self):
        """连接"""
        try:
            port = self.view.get_port()
            self.comm_manager.connect(port=port)
            self.view.set_connect()
            self.svc.start_handshake()
        except Exception as e:
            logger.error(f"连接失败: {e}")
            self.connection_status.emit("错误")
        else:
            self.connection_status.emit("已打开")

    def on_disconnect(self):
        """断开连接"""
        try:
            self.svc.stop_handshake()
            self.comm_manager.disconnect()
            self.view.set_disconnect()
        except Exception as e:
            logger.error(f"断开连接失败: {e}")
            self.connection_status.emit("错误")
        else:
            self.connection_status.emit("已关闭")

    def on_refresh_ports(self):
        """刷新端口"""
        ports = self.comm_manager.list_ports()
        self.view.refresh_ports(ports)
