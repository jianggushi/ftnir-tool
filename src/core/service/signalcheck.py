import logging
import time
import numpy as np
from collections import deque

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager
from config.types import (
    LightStabilityData,
    LaserStabilityData,
    SpectrumData,
    InterferenceData,
)
from core.processor.interference import FFTProcessor

from .base import BaseService, parse_interference_data


logger = logging.getLogger(__name__)


class LightStabilityService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()
        self._fft_processor = FFTProcessor()

        self.comm_manager = comm_manager
        self.comm_manager.register_handler(Command.CHECK_LIGHT_STABILITY_RES, self)

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
        self.comm_manager.send_message(Command.CHECK_LIGHT_STABILITY)

    def stop_check(self):
        self.comm_manager.send_message(Command.CHECK_STOP)


class WaveAccuracyService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()
        self._fft_processor = FFTProcessor()

        self.comm_manager = comm_manager
        self.comm_manager.register_handler(
            Command.CHECK_STANDARD_WAVE_ACCURACY_RES, self
        )

    def handle(self, msg: RawMessage):
        if msg.command != Command.CHECK_STANDARD_WAVE_ACCURACY_RES:
            return
        try:
            points = parse_interference_data(msg.data)
            interference_data = np.array(points, dtype=np.float32)
            spectrum_data = self._fft_processor.process(interference_data)

            # save data
            # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

            # run callbacks
            data = LightStabilityData(
                interference_data,
                0,
                spectrum_data,
                0,
            )
            self._run_callbacks(data)
        except Exception as e:
            logger.error(f"failed to handle message {msg.command}: {e}")

    def start_check(self):
        self.comm_manager.send_message(Command.CHECK_STANDARD_WAVE_ACCURACY)

    def stop_check(self):
        self.comm_manager.send_message(Command.CHECK_STOP)


class WaveRepeatabilityService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()
        self._fft_processor = FFTProcessor()

        self.comm_manager = comm_manager
        self.comm_manager.register_handler(
            Command.CHECK_STANDARD_WAVE_REPEATABILITY_RES, self
        )

    def handle(self, msg: RawMessage):
        if msg.command != Command.CHECK_STANDARD_WAVE_REPEATABILITY_RES:
            return
        try:
            points = parse_interference_data(msg.data)
            interference_data = np.array(points, dtype=np.float32)
            spectrum_data = self._fft_processor.process(interference_data)

            # save data
            # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

            # run callbacks
            data = LightStabilityData(
                interference_data,
                0,
                spectrum_data,
                0,
            )
            self._run_callbacks(data)
        except Exception as e:
            logger.error(f"failed to handle message {msg.command}: {e}")

    def start_check(self):
        self.comm_manager.send_message(Command.CHECK_STANDARD_WAVE_REPEATABILITY)

    def stop_check(self):
        self.comm_manager.send_message(Command.CHECK_STOP)


class LaserStabilityService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager
        self.comm_manager.register_handler(Command.CHECK_LASER_STABILITY_RES, self)

    def handle(self, msg: RawMessage):
        if msg.command != Command.CHECK_LASER_STABILITY_RES:
            return
        try:
            points = parse_interference_data(msg.data)
            interference_data = np.array(points, dtype=np.float32)
            # spectrum_data = self._fft_processor.process(interference_data)
            # 计算振幅
            amplitude = (np.max(interference_data) - np.min(interference_data)) / 2

            # run callbacks
            laser_stability_data = LaserStabilityData(
                interference_data,
                amplitude,
                None,
            )
            self._run_callbacks(laser_stability_data)
        except Exception as e:
            logger.error(f"failed to handle message {msg.command}: {e}")

    def start_check(self):
        self.comm_manager.send_message(Command.CHECK_LASER_STABILITY)

    def stop_check(self):
        self.comm_manager.send_message(Command.CHECK_STOP)
