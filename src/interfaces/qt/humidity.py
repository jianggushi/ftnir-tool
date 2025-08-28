import logging

from PySide6.QtCore import QObject, Signal, QTimer

from core.service.humidity import HumidityService
from config.types import HumidityData

from ui_qt.status_bar import StatusBarWidget

logger = logging.getLogger(__name__)


class HumidityController(QObject):
    humidity_str = Signal(str)

    def __init__(
        self,
        svc: HumidityService,
        view: None,
        status_bar: StatusBarWidget,
    ):
        super().__init__()

        self.svc = svc
        self.view = view

        self.svc.add_callback(self.receive_data)

        self.humidity_str.connect(status_bar.update_humidity_label)

        self.timer = QTimer(self)
        self.timer.setInterval(60 * 1000)
        self.timer.timeout.connect(self.get_humidity)

    # 获取湿度
    def get_humidity(self):
        try:
            self.svc.get_humidity()
        except Exception as e:
            logger.error(f"获取湿度失败: {e}")
            self.humidity_str.emit("错误")

    def start_polling(self):
        self.get_humidity()
        self.timer.start()

    def stop_polling(self):
        self.timer.stop()

    # 接收湿度数据
    def receive_data(self, data: HumidityData):
        self.humidity_str.emit(f"{data.data:.2f}")
