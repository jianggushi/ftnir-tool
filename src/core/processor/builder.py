from typing import Optional
from .base_processor import BaseProcessor
from .transforms import PhaseProcessor, WindowProcessor, FFTProcessor


class ProcessChainBuilder:
    """处理器链构建器"""

    def __init__(self):
        self._head: BaseProcessor = None
        self._tail: BaseProcessor = None

    def add_processor(self, processor: BaseProcessor) -> "ProcessChainBuilder":
        if not self._head:
            self._head = processor
            self._tail = processor
        else:
            self._tail.set_next(processor)
            self._tail = processor
        return self

    def build(self) -> BaseProcessor:
        if not self._head:
            raise ValueError("处理器链为空")
        return self._head


class StandardProcessChain:
    """标准处理链工厂"""

    @staticmethod
    def create(
        phase_offset: float = 0.0,
        window_type: str = "hann",
        use_zero_padding: bool = True,
    ) -> BaseProcessor:
        return (
            ProcessChainBuilder()
            .add_processor(PhaseProcessor().set_params(phase_offset))
            .add_processor(WindowProcessor(window_type))
            .add_processor(FFTProcessor(use_zero_padding))
            .build()
        )
