import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("001 _2_20250306T103419A.txt", comments="#")
wavenumbers = data[:, 0]
spectrum = data[:, 1]
print(spectrum)
interferogram = np.fft.irfft(spectrum)

N = len(wavenumbers)
# 波数间隔 (cm⁻¹)
wavenumber_step = np.mean(np.diff(wavenumbers))
# 计算光程差 (cm)
# 总的波数范围是 (N-1) * wavenumber_step
# 光程差的步长是 1 / (总波数范围)
opd_step = 1 / (N * wavenumber_step)
time_domain = np.linspace(0, opd_step, num=len(interferogram))

# 画图展示
plt.figure(figsize=(10, 6))
plt.plot(time_domain, interferogram, label="Interferogram (Real part)")
plt.xlabel("Optical Path Difference (a.u.)")
plt.ylabel("Intensity")
plt.title("Interferogram from Inverse Fourier Transform")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
