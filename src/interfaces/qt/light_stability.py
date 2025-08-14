from PySide6.QtCore import Slot, QObject, Signal

from core.service.light_stablity import LightStabilityService
from core.model.spectrum import LightStabilityData
from ui_qt.light_stability_widget import LightStabilityWidget


class LightStabilityController(QObject):
    light_stability_data = Signal(object)

    def __init__(self, svc: LightStabilityService, view: LightStabilityWidget):
        super().__init__()

        self.svc = svc
        self.view = view

        self.svc.add_callback(self.on_receive_data)

        self.light_stability_data.connect(self.view.update_plot)

        self.view.start_button.clicked.connect(self.start_check)
        self.view.stop_button.clicked.connect(self.stop_check)

    def start_check(self):
        self.svc.start_check()
        self.view.start_button.setEnabled(False)
        self.view.stop_button.setEnabled(True)

    def stop_check(self):
        self.svc.stop_check()
        self.view.start_button.setEnabled(True)
        self.view.stop_button.setEnabled(False)

    def on_receive_data(self, data: LightStabilityData):
        self.light_stability_data.emit(data)
