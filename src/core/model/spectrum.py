import numpy as np
from dataclasses import dataclass


@dataclass
class InterferenceData:
    data: np.ndarray
    max_value: float
    max_index: int
    min_value: float
    min_index: int


@dataclass
class SpectrumData:
    interference: np.ndarray
    spectrum: np.ndarray


@dataclass
class LightStabilityData:
    interference: InterferenceData
    max_max: float
    min_max: float
