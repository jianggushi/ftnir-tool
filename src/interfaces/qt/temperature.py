import logging

from PySide6.QtCore import QObject, Signal, QTimer

from core.service.temperature import TemperatureService
from core.model.spectrum import TemperatureData

from ui_qt.status_bar import StatusBarWidget

logger = logging.getLogger(__name__)


class TemperatureController(QObject):
    temperature_str = Signal(str)

    def __init__(
        self,
        svc: TemperatureService,
        view: None,
        status_bar: StatusBarWidget,
    ):
        super().__init__()

        self.svc = svc
        self.view = view

        self.svc.add_callback(self.receive_data)

        self.temperature_str.connect(status_bar.update_temperature_label)

        self.timer = QTimer(self)
        self.timer.setInterval(60 * 1000)
        self.timer.timeout.connect(self.get_temperature)

    # 获取温度
    def get_temperature(self):
        try:
            self.svc.get_temperature()
        except Exception as e:
            logger.error(f"获取温度失败: {e}")
            self.temperature_str.emit("错误")

    def start_polling(self):
        self.get_temperature()
        self.timer.start()

    def stop_polling(self):
        self.timer.stop()

    # 接收温度数据
    def receive_data(self, data: TemperatureData):
        self.temperature_str.emit(f"{data.data:.2f}")
