from PySide6.QtCore import Slot, QObject, Signal

from core.service.collect import CollectService
from core.model.types import CollectData
from ui_qt.control_collect import CollectWidget
from ui_qt.spectrum_figure import SpectrumFigureWidget


class CollectController(QObject):
    collect_data = Signal(object)

    def __init__(
        self,
        svc: CollectService,
        view: CollectWidget,
        spectrum_figure: SpectrumFigureWidget,
    ):

        super().__init__()

        self.svc = svc
        self.view = view
        self.spectrum_figure = spectrum_figure

        self.svc.add_callback(self.on_receive_data)

        self.collect_data.connect(self.view.on_receive_data)
        self.collect_data.connect(self.spectrum_figure.on_receive_data)

        self.view.start_button.clicked.connect(self.on_start_collect)
        self.view.stop_button.clicked.connect(self.on_stop_collect)

    def on_start_collect(self):
        continuous_mode = self.view.get_continuous_mode()
        num = self.view.get_collect_num()

        if self.view.dark_noise_radio.isChecked():
            self.svc.collect_dark_noise(num, continuous_mode)
        elif self.view.background_radio.isChecked():
            self.svc.collect_background(num, continuous_mode)
        elif self.view.sample_radio.isChecked():
            self.svc.collect_sample(num, continuous_mode)

        self.view.start_collect()

    def on_stop_collect(self):
        self.svc.stop_collect()
        self.view.stop_collect()

    def on_receive_data(self, data: CollectData):
        self.collect_data.emit(data)
