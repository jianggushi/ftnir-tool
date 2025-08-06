import numpy as np
from .base_processor import BaseProcessor


class FFTProcessor(BaseProcessor):
    def __init__(self, zero_padding: bool = False):
        super().__init__()
        self._zero_padding = zero_padding

    def process(self, data: np.ndarray) -> np.ndarray:
        y1 = np.fft.rfft(data, norm="forward")
        y2 = np.abs(y1)

        return self._process_next(y2)
