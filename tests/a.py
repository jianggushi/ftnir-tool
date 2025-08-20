import numpy as np
from scipy.integrate import simpson
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift


# ----------------------------------------------------------------------------
# 1. 原始代码：模拟光谱和干涉信号 (保持不变)
# ----------------------------------------------------------------------------
def simulate_interferogram_with_peaks(
    nu,
    peaks=None,
    delta_range=(-0.001, 0.001),
    n_delta=1000,
    noise_level=0.0,
):
    """
    模拟 FT-NIR 干涉信号，并自动生成高斯吸收峰光谱
    """
    S = np.ones_like(nu)
    if peaks is not None:
        for peak in peaks:
            center = peak.get("center", 0)
            width = peak.get("width", 50)
            amplitude = peak.get("amplitude", 0.5)
            S -= amplitude * np.exp(-0.5 * ((nu - center) / width) ** 2)
    delta_cm = np.linspace(delta_range[0], delta_range[1], n_delta)
    I = np.zeros_like(delta_cm)
    dc_offset = simpson(S, nu)
    for i, d in enumerate(delta_cm):
        ac_component = simpson(S * np.cos(2 * np.pi * nu * d), nu)
        I[i] = dc_offset + ac_component
    if noise_level > 0:
        I += np.random.normal(0, noise_level, size=I.shape)
    return delta_cm, I, S


# ----------------------------------------------------------------------------
# -- 主程序 --
# ----------------------------------------------------------------------------

# -- A. 生成原始数据 --
nu = np.linspace(4000, 10000, 2000)
peaks = [
    {"center": 5000, "width": 50, "amplitude": 0.5},
    {"center": 5500, "width": 50, "amplitude": 0.8},
    {"center": 7000, "width": 80, "amplitude": 0.7},
]
delta, I, S = simulate_interferogram_with_peaks(
    nu,
    peaks=peaks,
    delta_range=(-0.02, 0.02),
    n_delta=16384,
    noise_level=0.01,
)

# ----------------------------------------------------------------------------
# 2. 核心步骤：傅里叶变换（包含切趾）
# ----------------------------------------------------------------------------

# 步骤 1: 去除直流分量
I_ac = I - np.mean(I)

# 【【【 新增步骤 1.5: 切趾处理 (Apodization) 】】】
# 创建一个三角窗函数
# np.bartlett(M) 会生成一个长度为 M 的三角窗
triangular_window = np.bartlett(len(I_ac))
# 将干涉图与窗函数相乘
I_apodized = I_ac * triangular_window


# 步骤 2: 对两种干涉图分别进行FFT
# A. 无切趾
spectrum_complex_no_apod = fftshift(fft(I_ac))
# B. 有切趾
spectrum_complex_apod = fftshift(fft(I_apodized))

# 步骤 3: 计算波数轴 (两种情况共用)
n_points = len(I_ac)
sampling_interval = delta[1] - delta[0]
wavenumber_axis = fftshift(fftfreq(n_points, d=sampling_interval))

# 提取正波数部分的光谱
positive_indices = wavenumber_axis >= 0
wavenumber_reconstructed = wavenumber_axis[positive_indices]

# 无切趾的光谱强度
spectrum_no_apod = np.abs(spectrum_complex_no_apod[positive_indices])
# 有切趾的光谱强度
spectrum_apod = np.abs(spectrum_complex_apod[positive_indices])


# ----------------------------------------------------------------------------
# 3. 绘图比较
# ----------------------------------------------------------------------------
plt.figure(figsize=(12, 7))
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

# 绘制原始模拟光谱
plt.plot(nu, S, "r-", linewidth=3, label="原始模拟光谱 (Original)")

# 绘制无切趾的重构光谱
spectrum_no_apod_norm = spectrum_no_apod / np.max(spectrum_no_apod)
plt.plot(
    wavenumber_reconstructed,
    spectrum_no_apod_norm,
    "b-",
    alpha=0.6,
    label="重构光谱 - 无切趾 (Ringing)",
)

# 绘制有切趾的重构光谱
spectrum_apod_norm = spectrum_apod / np.max(spectrum_apod)
# plt.plot(
#     wavenumber_reconstructed,
#     spectrum_apod_norm,
#     "g-",
#     linewidth=1.5,
#     label="重构光谱 - 三角切趾 (Apodized)",
# )

jxj_y = np.abs(np.fft.rfft(I))
jxj_y_2 = jxj_y / np.max(jxj_y)
plt.plot(
    wavenumber_reconstructed,
    jxj_y_2.tolist()[:-1],
    "g-",
    linewidth=1.5,
    label="jxj",
)
print(jxj_y_2)


# 图表美化
plt.title("切趾对光谱振铃效应的抑制", fontsize=16)
plt.xlabel("波数 (cm⁻¹)", fontsize=12)
plt.ylabel("归一化强度", fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle="--", alpha=0.6)
plt.xlim(4000, 10000)
plt.ylim(0, 1.1)
plt.tight_layout()
plt.show()
