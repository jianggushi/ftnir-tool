import enum
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


class WindowType(enum.Enum):
    """
    窗口类型
    """

    RECTANGLE = "boxcar"
    TRIANGLE = "triang"
    GAUSSIAN = "gaussian"
    HAMMING = "hamming"
    HANNING = "hann"
    BLACKMANHARRIS = "blackmanharris"


class WindowProcessor(BaseProcessor):
    """
    窗口处理器
    """

    def __init__(self, window_type: WindowType):
        super().__init__()
        self.window_type = window_type

    def process(self, data: np.ndarray) -> np.ndarray:
        if self.window_type == WindowType.GAUSSIAN:
            window = signal.get_window(
                (self.window_type.value, len(data) / 8), len(data)
            )
        else:
            window = signal.get_window(self.window_type.value, len(data))
        return data * window


class FFTProcessor(BaseProcessor):
    def __init__(self, zero_padding: bool = False):
        super().__init__()
        self._zero_padding = zero_padding

    def process(self, data: np.ndarray) -> np.ndarray:
        y1 = np.fft.rfft(data, norm="forward")
        y2 = np.abs(y1)

        return self._process_next(y2)
