import logging
import time
import numpy as np
from collections import deque

from comm.protocol.parser import RawMessage, Command
from core.model.spectrum import LightStabilityData

from .interference import InterferenceHandler
from core.processor.fft_processor import FFTProcessor


logger = logging.getLogger(__name__)


class LightStabilityHandler(InterferenceHandler):
    def __init__(self):
        super().__init__()
        self._fft_processor = FFTProcessor()

        self._data_buffer = deque(maxlen=100)
        self.max_max = 0
        self.min_max = float("inf")

    def handle(self, msg: RawMessage):
        if msg.command != Command.CHECK_LIGHT_STABILITY_RES:
            return
        try:
            points = self._parse_spectrum_data(msg.data)
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


if __name__ == "__main__":
    pass
