import numpy as np
from scipy.integrate import simpson
from scipy.signal import windows
from scipy.signal import detrend
import matplotlib.pyplot as plt

res = np.loadtxt("12.txt", delimiter=",", comments="#")

# 光谱波数
nu = res[:, 0]
# 光谱强度
Snu = res[:, 1]
# print(Snu)

opd = (-0.0625, 0.0625)  # 光程差范围
sample_num = 16384  # 采样点数

x = np.linspace(opd[0], opd[1], sample_num)
print(x.shape, x)

nu_x_matrix = np.outer(nu, x)

print(nu_x_matrix.shape)

cos_matrix = np.cos(2 * np.pi * nu_x_matrix)

print(cos_matrix.shape)

d_nu = 3.078696
interferogram = np.dot(Snu, cos_matrix) * d_nu
print(interferogram.shape)
print(interferogram)
np.savetxt("interferogram.txt", interferogram)

plt.plot(interferogram)
# plt.plot(interferogram_detrend)
plt.show()


interferogram_detrend = detrend(interferogram, type="constant")
print(interferogram_detrend)
interferogram = interferogram_detrend


# # 找到zpd位置
# zpd_index = np.argmax(interferogram)
# print(zpd_index)

# N = len(interferogram)

# # 加窗
# w = windows.hann(N)
# interferogram = interferogram * w

# # 补零
# interf_shifted = np.roll(interferogram, N // 2 - zpd_index)
# M = 1 << (N - 1).bit_length()
# M = M * 2
# padded = np.zeros(M, dtype=float)
# start = (M - N) // 2
# padded[start : start + N] = interf_shifted

# interferogram = padded
# plt.plot(interferogram)
# plt.show()


# centered_interferogram = np.roll(interferogram, -zpd_index)
# print(centered_interferogram)
# plt.plot(interferogram)
# plt.plot(centered_interferogram)
# plt.show()

centered_interferogram = np.fft.ifftshift(interferogram)
complex_spectrum = np.fft.fft(centered_interferogram)
complex_spectrum_shifted = np.fft.fftshift(complex_spectrum)
corrected_spectrum = np.abs(complex_spectrum_shifted)

# corrected_spectrum = corrected_spectrum[len(corrected_spectrum) // 2 :]

# plt.plot(interferogram)
plt.plot(corrected_spectrum)
plt.show()

freqs = np.fft.fftfreq(sample_num, d=x[1] - x[0])
freqs = np.fft.fftshift(freqs)
print(freqs)
mask = (freqs >= 4000) & (freqs <= 11995)

print(mask)
sigma = freqs[mask]
print(sigma)
plt.plot(sigma, corrected_spectrum[mask])
plt.show()
np.savetxt("corrected_spectrum.txt", corrected_spectrum)


# apod_window = windows.hann(16384)
# apodized_interferogram = centered_interferogram * np.roll(apod_window, -zpd_index)

# complex_spectrum = np.fft.fft(apodized_interferogram)

# magnitude_spectrum = np.abs(complex_spectrum)

# print(magnitude_spectrum)


# plt.plot(magnitude_spectrum)

# # np.fft.ifftshift(interferogram)

# # plt.plot(np.abs(np.fft.fftshift(np.fft.fft(interferogram))))

# plt.show()


# # print(sample_points.shape, sample_points[None, :].shape)
# # print(sample_points)


# # dc = simpson(Snu, x=nu) if include_dc else 0.0

# cos_kernel = np.cos(2 * np.pi * nu[:, None] * sample_points[None, :])
# print(cos_kernel.shape)
# # print(cos_kernel)
# h = Snu[:, None] * cos_kernel
# print(h.shape)
# # print(h)

# I_mod = simpson(Snu[:, None] * cos_kernel, x=nu, axis=0)
# print(I_mod.shape)
# print(I_mod)
# I_mod = I_mod + simpson(Snu, x=nu)


# print(Snu.shape)
# print(Snu)

# res = np.fft.ifft(Snu)
# print(res)
# print(np.fft.fftshift(res))

# import matplotlib.pyplot as plt

# plt.plot(np.abs(res))
# plt.show()

plt.subplot(2, 1, 1)
plt.plot(interferogram)
plt.subplot(2, 1, 2)
plt.plot(sigma, corrected_spectrum[mask])
plt.show()
