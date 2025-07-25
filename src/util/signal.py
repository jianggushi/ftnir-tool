import numpy as np
import matplotlib.pyplot as plt


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
