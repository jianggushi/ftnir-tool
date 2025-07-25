from abc import ABC, abstractmethod
import numpy as np


class BaseProcessor(ABC):
    """base processor class"""

    def __init__(self):
        self._next_processor: BaseProcessor = None

    @abstractmethod
    def process(self, data: np.ndarray) -> np.ndarray:
        """process data"""
        pass

    def set_next(self, processor: "BaseProcessor") -> "BaseProcessor":
        """set next processor"""
        self._next_processor = processor
        return processor

    def _process_next(self, data: np.ndarray) -> np.ndarray:
        """"""
        if self._next_processor:
            return self._next_processor.process(data)
        return data
