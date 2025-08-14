from PySide6.QtCore import Slot, QObject, Signal

from core.service.collect import CollectService
from core.model.spectrum import SpectrumData
from ui_qt.collect_widget import CollectWidget
from ui_qt.interference_figure import InterferenceFigureWidget


class CollectController(QObject):
    collect_data = Signal(object)

    def __init__(
        self,
        svc: CollectService,
        view: CollectWidget,
        interference_figure: InterferenceFigureWidget,
    ):

        super().__init__()

        self.svc = svc
        self.view = view
        self.interference_figure = interference_figure

        self.svc.add_callback(self.on_receive_data)

        self.collect_data.connect(self.view.on_receive_data)
        self.collect_data.connect(self.interference_figure.on_receive_data)

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

    def on_receive_data(self, data: SpectrumData):
        self.collect_data.emit(data)
