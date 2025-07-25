import numpy as np
from typing import Optional
from scipy import signal


class PhaseCorrection:
    def __init__(self):
        self._phase_offset: float = 0.0

    def set_params(self, phase_offset: float):
        """设置相位校正参数

        Args:
            phase_offset: 相位偏移量（弧度）
        """
        self._phase_offset = phase_offset

    def apply(self, data: np.ndarray) -> np.ndarray:
        """应用相位校正

        Args:
            data: 输入数据

        Returns:
            相位校正后的数据
        """
        # 使用希尔伯特变换获取解析信号
        analytic_signal = signal.hilbert(data)
        # 应用相位校正
        corrected_signal = np.real(analytic_signal * np.exp(-1j * self._phase_offset))
        return corrected_signal


class WindowFunction:
    """窗函数处理类"""

    WINDOW_TYPES = {
        "hann": np.hanning,
        "hamming": np.hamming,
        "blackman": np.blackman,
        "kaiser": lambda N: np.kaiser(N, beta=14),
        "none": lambda N: np.ones(N),
    }

    def __init__(self):
        self._window_type: str = "none"
        self._window_func = self.WINDOW_TYPES["none"]

    def set_window_type(self, window_type: str):
        """设置窗函数类型

        Args:
            window_type: 窗函数类型，可选：'hann', 'hamming', 'blackman', 'kaiser', 'none'
        """
        if window_type not in self.WINDOW_TYPES:
            raise ValueError(f"不支持的窗函数类型: {window_type}")
        self._window_type = window_type
        self._window_func = self.WINDOW_TYPES[window_type]

    def apply(self, data: np.ndarray) -> np.ndarray:
        """应用窗函数

        Args:
            data: 输入数据

        Returns:
            加窗后的数据
        """
        window = self._window_func(len(data))
        return data * window


class FourierTransform:
    """傅里叶变换处理类"""

    def __init__(self):
        self._zero_padding: bool = False

    def set_params(self, zero_padding: bool = False):
        """设置FFT参数

        Args:
            zero_padding: 是否使用零填充
        """
        self._zero_padding = zero_padding

    def apply(self, data: np.ndarray) -> np.ndarray:
        """应用傅里叶变换

        Args:
            data: 输入数据

        Returns:
            频谱数据
        """
        n = len(data)
        if self._zero_padding:
            # 找到最接近的2的幂
            n_fft = 1 << (n - 1).bit_length()
            if n_fft < n:
                n_fft *= 2
        else:
            n_fft = n

        # 执行FFT
        spectrum = np.fft.fft(data, n=n_fft)

        # 计算频率轴
        freqs = np.fft.fftfreq(n_fft)

        # 取正频率部分
        positive_freq_idxs = np.where(freqs >= 0)
        spectrum = np.abs(spectrum[positive_freq_idxs])

        return spectrum
