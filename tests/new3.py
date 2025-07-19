import numpy as np
import matplotlib.pyplot as plt

# 读取光谱数据文件（省略头部处理，只处理数据）
file_path = "001 _2_20250306T103419A.txt"

# 读取数据部分，跳过以#开头的元数据行
data = []
with open(file_path, "r") as f:
    for line in f:
        if not line.startswith("#") and line.strip():
            parts = line.strip().split()
            if len(parts) == 2:
                try:
                    wavenumber = float(parts[0])  # 单位 cm^-1
                    intensity = float(parts[1])
                    data.append((wavenumber, intensity))
                except ValueError:
                    continue

data = np.array(data)
wavenumbers = data[:, 0]
spectrum = data[:, 1]

# 按波数从低到高排序（如果已是升序可跳过）
sort_idx = np.argsort(wavenumbers)
wavenumbers = wavenumbers[sort_idx]
spectrum = spectrum[sort_idx]

# 傅里叶逆变换（得到干涉图）
interferogram = np.fft.ifft(np.fft.ifftshift(spectrum))
time_domain = np.fft.fftfreq(len(spectrum), d=(wavenumbers[1] - wavenumbers[0]))
time_domain = np.fft.fftshift(time_domain)

# 画图展示
plt.figure(figsize=(10, 6))
plt.plot(time_domain, interferogram.real, label="Interferogram (Real part)")
plt.xlabel("Optical Path Difference (a.u.)")
plt.ylabel("Intensity")
plt.title("Interferogram from Inverse Fourier Transform")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
