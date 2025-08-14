import logging

from PySide6.QtCore import QObject, Signal

from core.service.hardware import HardwareService
from ui_qt.control_widget import HardwareSettingWidget

logger = logging.getLogger(__name__)


class HardwareController(QObject):
    def __init__(
        self,
        svc: HardwareService,
        view: HardwareSettingWidget,
    ):
        super().__init__()

        self.svc = svc
        self.view = view

        self.view.save_button.clicked.connect(self.on_setting_save)

    def on_setting_save(self):
        setting = self.view.get_settings()
        self.svc.set_hardware_setting(setting)
