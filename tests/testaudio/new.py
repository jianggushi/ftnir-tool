import numpy as np
import matplotlib.pyplot as plt

pcm_data = np.fromfile("iat_pcm_16k.pcm", dtype=np.int16)
sample_rate = 16000
num_samples = pcm_data.shape[0]
duration = num_samples / sample_rate

# 生成时间轴
time_axis = np.linspace(0, duration, num=num_samples)

# # 绘图
# plt.figure(figsize=(12, 4))
# plt.plot(time_axis, pcm_data, linewidth=0.5)
# plt.title("PCM Audio Waveform")
# plt.xlabel("Time (s)")
# plt.ylabel("Amplitude")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# 计算 FFT（只取正频率部分）
fft_res = np.fft.rfft(pcm_data)
fft_res2 = np.fft.fft(pcm_data)
freq_axis = np.fft.rfftfreq(num_samples, d=1 / sample_rate)
print(freq_axis)
magnitude = np.abs(fft_res)

# # 绘制频谱
# plt.figure(figsize=(12, 4))
# plt.plot(freq_axis, magnitude, linewidth=0.5)
# plt.title("Frequency Spectrum (FFT) of PCM Audio")
# plt.xlabel("Frequency (Hz)")
# plt.ylabel("Magnitude")
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# irfft 会将正频率部分的实数序列映射回时域的实值信号
reconstructed = np.fft.irfft(fft_res, n=len(pcm_data))
time_axis = np.linspace(0, len(pcm_data) / sample_rate, num=len(pcm_data))
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time_axis, pcm_data, linewidth=0.5)
plt.title("Original Waveform")
plt.ylabel("Amplitude")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(time_axis, reconstructed, linewidth=0.5)
plt.title("Reconstructed from Magnitude Only")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()
