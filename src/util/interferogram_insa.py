import numpy as np
from scipy.integrate import simpson
from scipy.signal import windows
from scipy.signal import detrend
import matplotlib.pyplot as plt

N = 10000


def simulate_sample_interferogram(
    filename: str,
):

    # 定义光程差范围
    opd = (-0.1625, 0.1625)
    # 定义采样点数
    sample_num = N

    data = np.loadtxt(filename, delimiter=",", comments="#")
    # nu 波数，Snu 强度
    nu, Snu = data[:, 0], data[:, 1]
    # d_nu 波数间隔
    d_nu = np.mean(np.diff(nu))
    # 生成等光程差的采样点
    x = np.linspace(opd[0], opd[1], sample_num)
    # 数值积分得到干涉图
    cos_matrix = np.cos(2 * np.pi * np.outer(nu, x))
    interferogram = np.dot(Snu, cos_matrix) * d_nu

    return x, interferogram


def simulate_sample_interferogram_with_noise(
    filename: str,
    noise_level: float = 0.001,
    seed: int = None,
):
    x, interferogram = simulate_sample_interferogram(filename)
    # 增加高斯噪声
    rng = np.random.default_rng(seed)
    noise_std = np.max(np.abs(interferogram)) * noise_level
    noise = rng.normal(0, noise_std, interferogram.shape)

    interferogram = interferogram + noise

    return x, interferogram


if __name__ == "__main__":
    # fig, ax = plt.subplots()
    x, interferogram = simulate_sample_interferogram(
        "data/insa/001 _2_20250306T103419.txt"
    )
    # plt.subplot(2, 1, 1)
    # plt.plot(x, interferogram)

    res = np.fft.rfft(interferogram)
    plt.subplot(2, 1, 1)
    plt.plot(np.abs(res))

    phase = np.angle(res)
    plt.subplot(2, 1, 2)
    plt.plot(phase)

    # res1 = np.fft.rfft(interferogram)
    # plt.subplot(2, 1, 1)
    # plt.plot(np.abs(res1))

    # res2 = np.fft.rfft(interferogram, norm="forward")
    # plt.subplot(2, 1, 2)
    # plt.plot(np.abs(res2))

    # sample_num = N
    # freqs = np.fft.rfftfreq(sample_num, d=x[1] - x[0])
    # mask = (freqs >= 4000) & (freqs < 12000)
    # print(x[1] - x[0])
    # print(freqs[mask].shape)

    # # plt.subplot(2, 1, 2)
    # plt.xlim(12000, 4000)
    # plt.plot(freqs[mask], np.abs(res1)[mask])

    # res1 = np.fft.ifftshift(interferogram)
    # res1 = np.fft.fft(res1)
    # res1 = np.fft.fftshift(res1)
    # plt.subplot(2, 1, 2)
    # plt.plot(np.abs(res1))

    # print(np.fft.rfft(interferogram), np.fft.rfft(interferogram).shape)

    # print(np.equal(np.abs(res), np.abs(res1)))

    # print(np.linspace(1, 12000, 3900, endpoint=False))

    plt.show()
