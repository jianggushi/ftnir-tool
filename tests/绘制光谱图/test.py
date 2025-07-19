import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

# 实际使用时，请替换为你的文件路径
data = np.loadtxt("GEB0062 250306006 2mm_185_20250306T165159A.txt")

# print(data)

# 分离波数和吸收度
wavenumbers = data[:, 0]
absorbance = data[:, 1]

print(wavenumbers)
print(absorbance)

plt.plot(wavenumbers, absorbance, 'b-', linewidth=1)
plt.title('原始近红外光谱 (波数-吸收度)')
plt.xlabel('波数 (cm^-1)')
plt.ylabel('吸收度')
plt.grid(True, alpha=0.3)
plt.show()

# # 检查波数是否等间距
# delta_wavenumber = wavenumbers[1] - wavenumbers[0]
# print(f"波数间隔: {delta_wavenumber} cm^-1")

# # 确保波数是递增的
# if np.any(np.diff(wavenumbers) < 0):
#     print("警告: 波数不是递增的，正在排序...")
#     sort_idx = np.argsort(wavenumbers)
#     wavenumbers = wavenumbers[sort_idx]
#     absorbance = absorbance[sort_idx]

# # 傅里叶逆变换前的预处理
# # 1. 零填充以提高变换分辨率
# original_length = len(wavenumbers)
# # 填充到下一个2的幂次长度，提高FFT效率
# padded_length = 2 ** (int(np.ceil(np.log2(original_length))) * 2)
# print(f"原始数据长度: {original_length}, 填充后长度: {padded_length}")

# # 创建等间距的波数数组（如果原始数据不是完全等间距的）
# min_wavenumber = wavenumbers[0]
# max_wavenumber = wavenumbers[-1]
# padded_wavenumbers = np.linspace(min_wavenumber, max_wavenumber, padded_length)

# # 插值到等间距的波数网格
# absorbance_interp = np.interp(padded_wavenumbers, wavenumbers, absorbance)

# # 2. 对称处理（傅里叶变换假设对称性）
# # 由于我们只有正波数部分，需要创建对称数据
# spectrum = np.zeros(padded_length * 2)
# spectrum[:padded_length] = absorbance_interp
# spectrum[padded_length:] = absorbance_interp[::-1]  # 镜像对称

# # 3. 应用傅里叶逆变换
# interferogram = np.fft.irfft(spectrum)

# # 4. 缩放和处理干涉图
# # 由于光谱数据通常表示为吸收度，需要转换为透射率或反射率
# # 这里假设数据已经是适合傅里叶变换的形式
# # 提取有用的时域数据（去除零填充和镜像部分的影响）
# time_domain = np.linspace(0, padded_length * 2, len(interferogram))
# useful_interferogram = interferogram[:padded_length]  # 提取原始长度对应的干涉图

# # # 绘制结果
# # plt.figure(figsize=(12, 8))

# # # 绘制原始光谱
# # plt.subplot(2, 1, 1)
# # plt.plot(wavenumbers, absorbance, 'b-', linewidth=1)
# # plt.title('原始近红外光谱 (波数-吸收度)')
# # plt.xlabel('波数 (cm^-1)')
# # plt.ylabel('吸收度')
# # plt.grid(True, alpha=0.3)

# # # 绘制干涉图
# # plt.subplot(2, 1, 2)
# # plt.plot(time_domain[:padded_length], useful_interferogram, 'r-', linewidth=1)
# # plt.title('傅里叶逆变换得到的干涉图 (时域)')
# # plt.xlabel('时间域')
# # plt.ylabel('干涉强度')
# # plt.grid(True, alpha=0.3)

# # plt.tight_layout()
# # plt.show()

# # # 保存干涉图数据
# # output_data = np.column_stack((time_domain[:padded_length], useful_interferogram))
# # np.savetxt("interferogram_data.txt", output_data, fmt="%.6f %.10f", 
# #            header="时间域 干涉强度", comments="")

# # print("干涉图数据已保存到interferogram_data.txt")