import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import irfft
from scipy.interpolate import interp1d


def load_spectrum_data(file_path):
    """
    从指定的文本文件中加载光谱数据。
    该函数会跳过以'#'开头的注释行。

    Args:
        file_path (str): 数据文件的路径。

    Returns:
        tuple: 包含两个 numpy 数组的元组 (wavenumbers, intensities)。
               如果文件无法读取，则返回 (None, None)。
    """
    try:
        data = np.loadtxt(file_path, comments="#")
        wavenumbers = data[:, 0]
        intensities = data[:, 1]
        return wavenumbers, intensities
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None, None


def main():
    """
    主函数，执行整个数据处理和变换流程。
    """
    # --- 1. 加载数据 ---
    # 请确保数据文件 '001 _2_20250306T103419A.txt' 与此脚本位于同一目录下。
    file_path = "001 _2_20250306T103419A.txt"
    wavenumbers, power_spectrum = load_spectrum_data(file_path)

    if wavenumbers is None:
        return

    # --- 2. 数据准备 ---
    # 文件头指明这是功率谱 (#Spectra: Power spectra)，因此需要取其平方根得到振幅谱。
    amplitude_spectrum = np.sqrt(power_spectrum)

    # --- 3. 插值到均匀网格 ---
    # 傅里叶逆变换需要均匀间隔的频率（波数）数据。
    # 我们将创建一个从 0 到数据最大波数的均匀网格。

    # 定义均匀网格的参数
    num_points = 8192  # 为FFT效率，通常选择2的幂次方，这里选择一个合理的值
    max_wavenumber = np.max(wavenumbers)
    # 创建一个均匀分布的波数数组，从 0 开始
    uniform_wavenumbers = np.linspace(0, max_wavenumber, num_points)

    # 创建插值函数
    # interp1d 默认在插值范围外会报错，我们设置 fill_value=0 来进行零填充。
    # 这对于从0到第一个实际数据点之间的区域是必需的。
    interp_func = interp1d(
        wavenumbers, amplitude_spectrum, bounds_error=False, fill_value=0.0
    )

    # 在均匀网格上获取插值后的振幅
    uniform_amplitude_spectrum = interp_func(uniform_wavenumbers)

    # --- 4. 执行傅里叶逆变换 ---
    # 使用 irfft (Inverse Real Fast Fourier Transform)，因为它适用于实数信号的单边频谱。
    interferogram = irfft(uniform_amplitude_spectrum)

    # --- 5. 可视化结果 ---
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # 绘制原始振幅谱
    ax1.plot(wavenumbers, amplitude_spectrum, label="原始振幅谱", color="crimson")
    ax1.set_title("原始近红外振幅谱", fontsize=16)
    ax1.set_xlabel("波数 (cm$^{-1}$)", fontsize=12)
    ax1.set_ylabel("振幅 (任意单位)", fontsize=12)
    ax1.legend()
    ax1.grid(True)

    # 绘制生成的干涉图
    # x轴是数据点索引，代表光程差的离散点
    ax2.plot(interferogram, label="生成的干涉图", color="darkblue")
    # 干涉图的中心爆 (Center Burst) 应该在索引0处
    ax2.set_title("生成的干涉图", fontsize=16)
    ax2.set_xlabel("光程差 (数据点索引)", fontsize=12)
    ax2.set_ylabel("强度 (任意单位)", fontsize=12)
    ax2.legend()
    ax2.grid(True)

    # 调整子图间距
    plt.tight_layout(pad=3.0)
    plt.show()


if __name__ == "__main__":
    main()
