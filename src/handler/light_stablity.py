import logging
import time
import numpy as np

from comm.protocol.parser import RawMessage, Command
from .interference import InterferenceHandler
from .processor.fft_processor import FFTProcessor

logger = logging.getLogger(__name__)


class LightStabilityHandler(InterferenceHandler):
    def __init__(self):
        super().__init__()
        self._fft_processor = FFTProcessor()

    def handle(self, msg: RawMessage):
        if msg.command != Command.CHECK_LIGHT_STABILITY_RES:
            return
        try:
            points = self._parse_spectrum_data(msg.data)
            interference_data = np.array(points, dtype=np.float32)

            spectrum_data = self._fft_processor.process(interference_data)

            # save data
            filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

            # run callbacks
            self._run_callbacks(
                {
                    "interference_data": interference_data,
                    "spectrum_data": spectrum_data,
                }
            )
        except Exception as e:
            logger.error(f"failed to handle message {msg.command}: {e}")


if __name__ == "__main__":
    pass
