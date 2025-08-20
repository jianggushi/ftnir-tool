import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

N = 4096


x = np.linspace(-0.01, 0.01, N)

# nu0 = 1.0 / 638 * 10**7
nu0 = 5000
print(nu0)
I0 = 1.0
I = I0 * (1 + np.cos(2 * np.pi * nu0 * x))

nu1 = np.abs(np.fft.fftshift(np.fft.fft(signal.detrend(I, type="constant"))))
dx = x[1] - x[0]
freqs = np.fft.fftshift(np.fft.fftfreq(N, d=dx))

plt.subplot(2, 1, 1)
plt.plot(x, I)

plt.subplot(2, 1, 2)
plt.plot(freqs, nu1)

plt.show()
