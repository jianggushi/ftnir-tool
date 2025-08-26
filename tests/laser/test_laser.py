import numpy as np
import matplotlib.pyplot as plt


def test_laser():
    # 模拟一个正弦信号
    f0 = 1.1
    x = np.linspace(-5, 5, 1000)
    signal = 2.0 * np.cos(2 * np.pi * f0 * x)  # 振幅=2

    # 计算振幅
    amplitude = (np.max(signal) - np.min(signal)) / 2
    assert abs(amplitude - 2.0) < 1e-5

    # 绘制信号
    plt.plot(x, signal)
    plt.show()


def test_laser_dc():
    # 模拟一个正弦信号
    f0 = 1.1
    x = np.linspace(-5, 5, 1000)
    signal = 2.0 * np.cos(2 * np.pi * f0 * x) + 2.35  # 振幅=2

    # 计算振幅
    amplitude = (np.max(signal) - np.min(signal)) / 2
    assert abs(amplitude - 2.0) < 1e-5

    # 绘制信号
    plt.plot(x, signal)
    plt.show()


def test_laser_noise():
    # 模拟一个正弦信号
    f0 = 1.1
    x = np.linspace(-5, 5, 1000)
    signal = 2.0 * np.cos(2 * np.pi * f0 * x) + 2.35  # 振幅=2

    # 加入噪声
    noise = np.random.normal(0, 0.25, 1000)
    signal += noise

    # 计算振幅
    amplitude = (np.max(signal) - np.min(signal)) / 2
    assert abs(amplitude - 2.0) < 1e-5

    # 绘制信号
    plt.plot(x, signal)
    plt.show()
