import numpy as np
from scipy.integrate import simpson
from scipy.signal import windows
from scipy.signal import detrend
import matplotlib.pyplot as plt

N = 3000


def simulate_sample_interferogram(
    filename: str,
):

    # 定义光程差范围
    opd = (-0.0625, 0.0625)
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


def simulate_laser_interferogram():
    # 模拟一个正弦信号
    x = np.linspace(-5, 5, 1000)

    y = 2.0 * np.cos(2 * np.pi * x)

    return x, y


def generate_test_signal(fs=1000, duration=1.0, amp=1.0, noise_level=0.2):
    """
    构造包含一路随机频率正弦信号和高斯噪声的测试信号。

    参数:
        fs (float):         采样率，单位 Hz。
        duration (float):   信号持续时间，单位秒。
        amp (float):        正弦信号的幅值。
        noise_level (float):噪声幅度系数。

    返回:
        t     (ndarray): 时间向量。
        sig   (ndarray): 构造出的信号。
        freq  (int):     随机选取的正弦信号频率。
    """
    # 在 [1, fs/2) 之间随机选取一个整数频率
    freq = np.random.randint(1, fs // 2)
    t = np.arange(0, duration, 1 / fs)
    sig = amp * np.sin(2 * np.pi * freq * t) + noise_level * np.random.randn(t.size)
    return t, sig, freq


if __name__ == "__main__":
    # fig, ax = plt.subplots()
    x, interferogram = simulate_sample_interferogram(
        "../data/insa/001 _2_20250306T103419.txt"
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
