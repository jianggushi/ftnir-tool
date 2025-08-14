import logging

from PySide6.QtCore import QObject, Signal

from core.service.light import LightService
from ui_qt.control_widget import LightWidget
from ui_qt.status_bar import StatusBarWidget

logger = logging.getLogger(__name__)


class LightController(QObject):
    light_status = Signal(str)
    laser_status = Signal(str)

    def __init__(
        self,
        svc: LightService,
        view: LightWidget,
        status_bar: StatusBarWidget,
    ):
        super().__init__()

        self.svc = svc
        self.view = view

        self.light_status.connect(status_bar.update_light_label)
        self.laser_status.connect(status_bar.update_laser_label)

        self.view.light_button.clicked.connect(self.on_light_toggle)
        self.view.laser_button.clicked.connect(self.on_laser_toggle)

    def on_light_toggle(self):
        try:
            if self.view.light_on:
                self.svc.turn_off_light()
                self.view.turn_off_light()
            else:
                self.svc.turn_on_light()
                self.view.turn_on_light()
        except Exception as e:
            logger.error(f"切换光源失败: {e}")
            self.light_status.emit("错误")
        else:
            if self.view.light_on:
                self.light_status.emit("已打开")
            else:
                self.light_status.emit("已关闭")

    def on_laser_toggle(self):
        try:
            if self.view.laser_on:
                self.svc.turn_off_laser()
                self.view.turn_off_laser()
            else:
                self.svc.turn_on_laser()
                self.view.turn_on_laser()
        except Exception as e:
            logger.error(f"切换激光失败: {e}")
            self.laser_status.emit("错误")
        else:
            if self.view.laser_on:
                self.laser_status.emit("已打开")
            else:
                self.laser_status.emit("已关闭")
