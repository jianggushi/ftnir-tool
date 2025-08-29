import logging

from PySide6.QtCore import QObject, Signal, Slot

from core.service.pwm import PwmService
from ui_qt.control_widget import PwmWidget

logger = logging.getLogger(__name__)


class PwmController(QObject):
    def __init__(
        self,
        svc: PwmService,
        view: PwmWidget,
    ):
        super().__init__()

        self.svc = svc
        self.view = view

        self.view.set_button.clicked.connect(self.on_set_pwm)

    @Slot()
    def on_set_pwm(self):
        cycle, duty = self.view.get_pwm_param()
        self.svc.set_pwm_param(cycle, duty)
