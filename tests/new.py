import numpy as np
import matplotlib.pyplot as plt


def read_spectrum_data(file_path):
    """
    读取光谱数据文件，跳过头部信息。

    Args:
        file_path (str): 数据文件路径。

    Returns:
        tuple: 包含波数和吸光度的一维数组。
    """
    wavenumbers = []
    absorbance = []
    with open(file_path, "r") as f:
        for line in f:
            # 跳过以 '#' 开头的注释行
            if line.strip().startswith("#"):
                continue

            # 分割数据并添加到列表中
            parts = line.split()
            if len(parts) == 2:
                try:
                    wavenumbers.append(float(parts[0]))
                    absorbance.append(float(parts[1]))
                except ValueError:
                    # 如果某一行无法转换为浮点数，则跳过
                    continue
    return np.array(wavenumbers), np.array(absorbance)


# --- 主程序 ---
file_path = "GEB0062 250306006 2mm_185_20250306T165159A.txt"  # 替换为您的文件路径

# 1. 读取数据
wavenumbers, absorbance = read_spectrum_data(file_path)

# 确保数据是按波数顺序排列的
sort_indices = np.argsort(wavenumbers)
wavenumbers = wavenumbers[sort_indices]
absorbance = absorbance[sort_indices]

print("absorbance")
print(absorbance)
# 2. 执行傅里叶逆变换 (IFFT)
# np.fft.ifft 会计算傅里叶逆变换
interferogram = np.fft.ifft(absorbance)

print("interferogram")
print(interferogram)

# 傅里叶逆变换的结果是复数，通常我们关心其实部或模
interferogram_real = np.real(interferogram)

# 3. 创建对应的光程差（时域）坐标
# 波数的分辨率决定了光程差的范围
N = len(wavenumbers)
# 波数间隔 (cm⁻¹)
wavenumber_step = np.mean(np.diff(wavenumbers))
# 计算光程差 (cm)
# 总的波数范围是 (N-1) * wavenumber_step
# 光程差的步长是 1 / (总波数范围)
opd_step = 1 / (N * wavenumber_step)
print(opd_step)
# 创建光程差坐标轴
opd = np.arange(N) * opd_step

# --- 4. 结果可视化 ---

# # 绘制原始光谱图
# plt.figure(figsize=(12, 6))

# plt.subplot(1, 2, 1)
# plt.plot(wavenumbers, absorbance)
# plt.title('近红外光谱图 (频域)')
# plt.xlabel('波数 (cm⁻¹)')
# plt.ylabel('吸光度')
# plt.grid(True)
# # 反转X轴，因为通常波数从大到小显示
# plt.gca().invert_xaxis()

# 绘制傅里叶逆变换后的干涉图
# 通常干涉图的中心点（零光程差）是最强的信号
# 使用 np.fft.fftshift 将零频分量（对应零光程差）移到中心
# plt.subplot(1, 2, 2)
plt.plot(opd, np.fft.fftshift(interferogram_real))
plt.title("干涉图 (时域)")
plt.xlabel("光程差 (cm)")
plt.ylabel("强度")
plt.grid(True)

plt.tight_layout()
plt.show()

# 打印部分干涉图数据
print("傅里叶逆变换后的部分干涉图数据 (实部):")
# 使用 fftshift 将中心点数据显示在前面
shifted_interferogram = np.fft.fftshift(interferogram_real)
print(shifted_interferogram[:10])
