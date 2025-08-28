import numpy as np
import matplotlib.pyplot as plt


# 采样点数
N = 1024
# 时间范围的半宽
T = 10.0

t = np.linspace(-T, T, N, endpoint=False)
print("采样点:", t)

# 频率 1Hz
f0 = 1.0
y0 = np.cos(2 * np.pi * f0 * t)
y = np.cos(2 * np.pi * f0 * t - 0.5)
# y = y0

print("原始信号:", y)

Y = np.fft.fft(y)
print("FFT结果", Y)

print("FFT结果的实部:", np.real(Y))
print("FFT结果的虚部:", np.imag(Y))

max_real_part = np.max(np.abs(np.real(Y)))
max_imag_part = np.max(np.abs(np.imag(Y)))

print("FFT结果的实部最大值:", max_real_part)
print("FFT结果的虚部最大值:", max_imag_part)

scale = max_real_part / max_imag_part

print("FFT结果的实部最大值与虚部最大值的比例:", f"{scale:.0f}")

# plt.plot(t, y0)
# plt.plot(t, y)
plt.plot(Y.real)
plt.plot(Y.imag)
plt.show()
