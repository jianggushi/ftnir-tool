from .base_processor import BaseProcessor


class PhaseProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self._phase_offset: float = 0.0

    def process(self, data: np.ndarray) -> np.ndarray:
        # 相位校正处理
        analytic_signal = signal.hilbert(data)
        corrected = np.real(analytic_signal * np.exp(-1j * self._phase_offset))
        return self._process_next(corrected)
