from PySide6.QtCore import Slot, QObject, Signal

from core.service.signal import LightStabilityService
from core.model.spectrum import LightStabilityData
from ui_qt.light_stability_widget import LightStabilityWidget
from core.model.engine import db
from core.model.light_stability import LightStabilityResult

from sqlalchemy import select, update


class LightStabilityController(QObject):
    light_stability_data = Signal(object)

    def __init__(self, svc: LightStabilityService, view: LightStabilityWidget):
        super().__init__()

        self.svc = svc
        self.view = view

        self.svc.add_callback(self.receive_data)

        self.light_stability_data.connect(self.view.on_receive_data)

        self.view.start_button.clicked.connect(self.start_check)
        self.view.stop_button.clicked.connect(self.stop_check)
        self.view.load_result_signal.connect(self.load_result)
        self.view.save_result_signal.connect(self.save_result)

    def start_check(self):
        self.svc.start_check()
        self.view.start_button.setEnabled(False)
        self.view.stop_button.setEnabled(True)

    def stop_check(self):
        self.svc.stop_check()
        self.view.start_button.setEnabled(True)
        self.view.stop_button.setEnabled(False)

    def receive_data(self, data: LightStabilityData):
        self.light_stability_data.emit(data)

    @Slot()
    def load_result(self):
        with db.session() as session:
            result = session.execute(select(LightStabilityResult).limit(1)).scalar()
        if result is None:
            return
        self.view.interference_figure.set_ref_max(result.interference_max_max)
        self.view.spectrum_figure.set_ref_max(result.spectrum_max_max)

    @Slot(object)
    def save_result(self, data: LightStabilityData):
        with db.session() as session:
            result = session.execute(select(LightStabilityResult).limit(1)).scalar()
            if result is None:
                session.add(
                    LightStabilityResult(
                        interference_max_max=data.interference_max_max,
                        spectrum_max_max=data.spectrum_max_max,
                    )
                )
            else:
                if (
                    data.interference_max_max > result.interference_max_max
                    or data.spectrum_max_max > result.spectrum_max_max
                ):
                    result.interference_max_max = data.interference_max_max
                    result.spectrum_max_max = data.spectrum_max_max
            self.view.interference_figure.set_ref_max(result.interference_max_max)
            self.view.spectrum_figure.set_ref_max(result.spectrum_max_max)
            session.commit()
