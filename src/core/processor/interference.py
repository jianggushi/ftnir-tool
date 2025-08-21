import numpy as np
from scipy import signal

from .base_processor import BaseProcessor


class RemoveDCProcessor(BaseProcessor):
    """
    去直流处理器
    """

    def __init__(self):
        super().__init__()

    def process(self, data: np.ndarray) -> np.ndarray:
        """
        参考：https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.detrend.html
        """
        return signal.detrend(data, type="constant")

    def process_v1(self, data: np.ndarray) -> np.ndarray:
        return data - np.mean(data)


class FFTProcessor(BaseProcessor):
    def __init__(self, zero_padding: bool = False):
        super().__init__()
        self._zero_padding = zero_padding

    def process(self, data: np.ndarray) -> np.ndarray:
        y1 = np.fft.rfft(data, norm="forward")
        y2 = np.abs(y1)

        return self._process_next(y2)
