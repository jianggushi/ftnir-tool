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
    def __init__(self):
        super().__init__()

    def process(self, data: np.ndarray) -> np.ndarray:
        spectrum = self.fft_abs(data)

        return self._process_next(spectrum)

    def fft_freq(self, n: int, resolution: float) -> np.ndarray:
        d = 1.0 / resolution / n
        freq = np.fft.fftshift(np.fft.fftfreq(n, d))
        return freq

    def fft_abs(self, data: np.ndarray) -> np.ndarray:
        N_original = len(data)
        N_padded = 2 ** int(np.ceil(np.log2(N_original)))

        # 计算FFT
        spectrum_complex = np.fft.fftshift(np.fft.fft(data))

        # 取模
        spectrum = np.abs(spectrum_complex)

        return spectrum

    def fft_mertz(self, data: np.ndarray) -> np.ndarray:
        N_original = len(data)
        N_padded = 2 ** int(np.ceil(np.log2(N_original)))

        # 进行FFT，得到复数谱
        spectrum_complex = np.fft.fftshift(np.fft.fft(data, N_padded))

        # 计算相位
        spectrum_phase = np.unwrap(np.angle(spectrum_complex))
        # 相位校正
        spectrum_corrected = np.abs(spectrum_complex) * np.cos(spectrum_phase)

        return spectrum_corrected[N_padded // 2 :]

    def fft_mertz_2(self, data: np.ndarray) -> np.ndarray:
        zpd_index = np.argmax(np.abs(data))  # 找到零光程差位置

        N_original = len(data)
        N_padded = 2 ** int(np.ceil(np.log2(N_original)))

        # 截取零光程差附近的2048个点
        N_center = 2048
        data_low = np.zeros(len(data))
        data_low[zpd_index - N_center // 2 : zpd_index + N_center // 2] = data[
            zpd_index - N_center // 2 : zpd_index + N_center // 2
        ]
        # 计算低分辨率FFT
        spectrum_low = np.fft.fft(data_low, N_padded)
        # 计算低分辨率相位谱
        spectrum_phase = np.angle(spectrum_low)
        # 计算全分辨率FFT
        spectrum_full = np.fft.fft(data, N_padded)
        # 相位校正
        spectrum_full_corrected = spectrum_full * np.exp(1j * spectrum_phase)

        spectrum = np.real(spectrum_full_corrected)

        return spectrum
