import numpy as np
from dataclasses import dataclass


@dataclass
class SpectrumData:
    interference: np.array
    spectrum: np.array
