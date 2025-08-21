import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
import math
from core.processor.interference import RemoveDCProcessor

processor = RemoveDCProcessor()


def test_remove_dc():
    t = np.linspace(-0.5, 0.5, 21)  # 时间轴
    x = np.sin(2 * np.pi * t) + 0.25  # 正弦信号+直流分量

    x_detrend = processor.process(x)

    assert abs(np.mean(x) - 0.25) < 1e-9
    assert abs(np.mean(x_detrend)) < 1e-9


def test_remove_dc_plot():
    t = np.linspace(-0.5, 0.5, 21)  # 时间轴
    x = np.sin(2 * np.pi * t) + 0.25  # 正弦信号+直流分量

    x_detrend = processor.process(x)

    assert abs(np.mean(x) - 0.25) < 1e-9
    assert abs(np.mean(x_detrend)) < 1e-9

    ax = plt.subplot()
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)

    ax.plot(t, x, label="x")
    ax.plot(t, x_detrend, label="x_detrend")

    plt.show()


def test_remove_dc_plot():
    t = np.linspace(-0.5, 0.5, 21)  # 时间轴
    x = np.sin(2 * np.pi * t) + 0.25  # 正弦信号+直流分量

    x_detrend = processor.process(x)

    assert abs(np.mean(x) - 0.25) < 1e-9
    assert abs(np.mean(x_detrend)) < 1e-9

    ax = plt.subplot()
    ax.axhline(0, color="black", linewidth=0.5)
    ax.axvline(0, color="black", linewidth=0.5)

    ax.plot(t, x, label="x")
    ax.plot(t, x_detrend, label="x_detrend")

    plt.show()


def test_remove_dc_fft():
    t = np.linspace(-0.5, 0.5, 21)  # 时间轴
    x = np.sin(2 * np.pi * t) + 0.25  # 正弦信号+直流分量

    x_detrend = signal.detrend(x, type="constant")

    assert abs(np.mean(x) - 0.25) < 1e-9
    assert abs(np.mean(x_detrend)) < 1e-9

    X = np.fft.rfft(x)
    X_detrend = np.fft.rfft(x_detrend)

    ax = plt.subplot()
    ax.plot(np.abs(X))
    ax.plot(np.abs(X_detrend))

    plt.show()
