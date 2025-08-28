import numpy as np
from dataclasses import dataclass
import enum


class ResolutionEnum(enum.Enum):
    R_0_2 = (1, "0.2")
    R_0_4 = (2, "0.4")
    R_0_8 = (3, "0.8")
    R_1_0 = (4, "1.0")
    R_2_0 = (5, "2.0")
    R_4_0 = (6, "4.0")
    R_8_0 = (7, "8.0")

    def __init__(self, num, label):
        self._value_ = num
        self.label = label

    @classmethod
    def from_label(cls, label: str):
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"{label!r} is not a valid {cls.__name__}")

    def to_float(self) -> float:
        return float(self.label)


class VelocityEnum(enum.Enum):
    V_200 = (1, "200")
    V_300 = (2, "300")
    V_500 = (3, "500")
    V_1000 = (4, "1000")
    V_2000 = (5, "2000")
    V_3000 = (6, "3000")

    def __init__(self, num, label):
        self._value_ = num
        self.label = label

    @classmethod
    def from_label(cls, label: str):
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"{label!r} is not a valid {cls.__name__}")


class ScanModeEnum(enum.Enum):
    S_1 = (1, "单向-单边")
    S_2 = (2, "单向-双边")
    S_3 = (3, "双向-单边")
    S_4 = (4, "双向-双边")

    def __init__(self, num, label):
        self._value_ = num
        self.label = label

    @classmethod
    def from_label(cls, label: str):
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"{label!r} is not a valid {cls.__name__}")


class DirectionEnum(enum.Enum):
    D_P = (1, "正向")
    D_N = (2, "反向")

    def __init__(self, num, label):
        self._value_ = num
        self.label = label

    @classmethod
    def from_label(cls, label: str):
        for member in cls:
            if member.label == label:
                return member
        raise ValueError(f"{label!r} is not a valid {cls.__name__}")


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
    freq_data: np.ndarray
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
