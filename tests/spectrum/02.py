import numpy as np
import matplotlib.pyplot as plt


def monochromatic_interferogram(nu0, I0=1.0, x_max=1.0, N=3000):
    """
    模拟单色光干涉信号
    :param nu0: 单色光波数 (cm^-1)
    :param I0: 平均强度
    :param x_max: 最大OPD(cm)
    :param N: 采样点数
    :return: x (OPD数组), I(x) (干涉信号)
    """
    # OPD 轴（对称，零点在中心）
    x = np.linspace(-x_max, x_max, N)
    # 单色干涉信号
    I = I0 * (1 + np.cos(2 * np.pi * nu0 * x))
    return x, I


# ====== 示例 ======
if __name__ == "__main__":
    nu0 = 5000  # cm^-1，对应 ~2000 nm
    x, I = monochromatic_interferogram(nu0)

    plt.plot(x, I)
    plt.title(f"单色光干涉信号 (ν₀ = {nu0} cm⁻¹)")
    plt.xlabel("OPD x (cm)")
    plt.ylabel("Intensity I(x)")
    plt.grid(True)
    plt.show()
