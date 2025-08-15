import logging
import time
import numpy as np
from collections import deque

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager
from core.model.spectrum import LightStabilityData, SpectrumData, InterferenceData
from core.processor.interference import FFTProcessor

from .base import BaseService, parse_interference_data


logger = logging.getLogger(__name__)


class LightStabilityService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager
        self._fft_processor = FFTProcessor()

        # self._data_buffer = deque(maxlen=100)
        self.interference_max_max = 0
        self.spectrum_max_max = 0

    def handle(self, msg: RawMessage):
        if msg.command != Command.CHECK_LIGHT_STABILITY_RES:
            return
        try:
            points = parse_interference_data(msg.data)
            interference_data = np.array(points, dtype=np.float32)
            spectrum_data = self._fft_processor.process(interference_data)

            max_value = np.max(interference_data)
            self.interference_max_max = max(max_value, self.interference_max_max)

            max_value = np.max(spectrum_data)
            self.spectrum_max_max = max(max_value, self.spectrum_max_max)

            # save data
            # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

            # run callbacks
            light_stability_data = LightStabilityData(
                interference_data,
                self.interference_max_max,
                spectrum_data,
                self.spectrum_max_max,
            )
            self._run_callbacks(light_stability_data)
        except Exception as e:
            logger.error(f"failed to handle message {msg.command}: {e}")

    def start_check(self):
        self.comm_manager.send_message(Command.CHECK_LIGHT_STABILITY, b"\01")

    def stop_check(self):
        self.comm_manager.send_message(Command.CHECK_STOP, b"\03")


class WaveAccuracyService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager
        self._fft_processor = FFTProcessor()

        self._data_buffer = deque(maxlen=100)
        self.max_max = 0
        self.min_max = float("inf")

    def handle(self, msg: RawMessage):
        if msg.command != Command.CHECK_STANDARD_WAVE_ACCURACY_RES:
            return
        try:
            points = parse_interference_data(msg.data)
            interference_data = np.array(points, dtype=np.float32)

            max_value = np.max(interference_data)
            self.max_max = max(max_value, self.max_max)
            self.min_max = min(max_value, self.min_max)

            # spectrum_data = self._fft_processor.process(interference_data)

            # save data
            # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

            # run callbacks
            light_stability_data = LightStabilityData(
                interference_data,
                self.max_max,
                self.min_max,
            )
            self._run_callbacks(light_stability_data)
        except Exception as e:
            logger.error(f"failed to handle message {msg.command}: {e}")

    def start_check(self):
        self.comm_manager.send_message(Command.CHECK_WAVE_ACCURACY, b"\02")

    def stop_check(self):
        self.comm_manager.send_message(Command.CHECK_STOP, b"\03")


class WaveRepeatabilityService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager
        self._fft_processor = FFTProcessor()

        self._data_buffer = deque(maxlen=100)
        self.max_max = 0
        self.min_max = float("inf")

    def handle(self, msg: RawMessage):
        if msg.command != Command.CHECK_STANDARD_WAVE_REPEATABILITY_RES:
            return
        try:
            points = parse_interference_data(msg.data)
            interference_data = np.array(points, dtype=np.float32)

            max_value = np.max(interference_data)
            self.max_max = max(max_value, self.max_max)
            self.min_max = min(max_value, self.min_max)

            # spectrum_data = self._fft_processor.process(interference_data)

            # save data
            # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

            # run callbacks
            light_stability_data = LightStabilityData(
                interference_data,
                self.max_max,
                self.min_max,
            )
            self._run_callbacks(light_stability_data)
        except Exception as e:
            logger.error(f"failed to handle message {msg.command}: {e}")

    def start_check(self):
        self.comm_manager.send_message(
            Command.CHECK_STANDARD_WAVE_REPEATABILITY, b"\03"
        )

    def stop_check(self):
        self.comm_manager.send_message(Command.CHECK_STOP, b"\03")
