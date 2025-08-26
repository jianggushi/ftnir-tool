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
    data: np.ndarray
    max_value: float
    max_index: int
    min_value: float
    min_index: int


@dataclass
class CollectData:
    interference_data: np.ndarray
    spectrum_data: np.ndarray


@dataclass
class LightStabilityData:
    interference_data: np.ndarray  # 干涉数据
    interference_max_max: float  # 干涉最大强度的最大值
    # interference_min_max: float  # 干涉最大强度的最小值
    spectrum_data: np.ndarray  # 光谱数据
    spectrum_max_max: float  # 光谱最大强度的最大值
    # spectrum_min_max: float  # 光谱最大强度的最小值


@dataclass
class LaserStabilityData:
    interference_data: np.ndarray  # 干涉数据
    amplitude: float  # 干涉数据的振幅

    spectrum_data: np.ndarray  # 光谱数据
    # spectrum_max_max: float  # 光谱最大强度的最大值
    # spectrum_min_max: float  # 光谱最大强度的最小值


@dataclass
class TemperatureData:
    data: float
    timestamp: int


@dataclass
class HumidityData:
    data: float
    timestamp: int


@dataclass
class HardwareData:
    resolution: int
    velocity: int
    direction: int
    scan_mode: int
