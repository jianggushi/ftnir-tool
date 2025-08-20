import numpy as np
from scipy.integrate import simpson
from scipy.signal import windows
from scipy.signal import detrend
import matplotlib.pyplot as plt

res = np.loadtxt("04.txt", delimiter=",", comments="#")
print(res.shape, res)
interferogram = res

interferogram_detrend = detrend(interferogram, type="constant")
print(interferogram_detrend)
interferogram = interferogram_detrend

centered_interferogram = np.fft.ifftshift(interferogram)
complex_spectrum = np.fft.fft(centered_interferogram)
complex_spectrum_shifted = np.fft.fftshift(complex_spectrum)
corrected_spectrum = np.abs(complex_spectrum_shifted)

plt.plot(corrected_spectrum)
plt.show()


N = len(interferogram)
freqs = np.fft.fftfreq(N, d=0.000005)
freqs = np.fft.fftshift(freqs)
print(freqs)
mask = (freqs >= 4000) & (freqs <= 12500)

print(mask)
sigma = freqs[mask]
print(sigma)
plt.plot(sigma, corrected_spectrum[mask])
plt.show()
