import numpy as np
import matplotlib.pyplot as plt

from core.processor.interference import FFTProcessor
from util.interferogram import simulate_sample_interferogram


def test_interferogram_background():
    x, y = simulate_sample_interferogram("data/insa/001 _2_20250306T103419_ref.txt")
    plt.plot(x, y)
    plt.show()


def test_interferogram_sample():
    x, y = simulate_sample_interferogram("data/insa/001 _2_20250306T103419_spec0.txt")
    plt.plot(x, y)
    plt.show()


def test_interferogram_background_fft():
    x, y = simulate_sample_interferogram("data/insa/001 _2_20250306T103419_ref.txt")
    fft = FFTProcessor()

    Y = fft.fft_abs(y)

    d = 1 / 8 / len(Y)
    X = np.fft.fftshift(np.fft.fftfreq(len(Y), d))

    mask = (X >= 4000) & (X <= 12000)

    print(mask)
    print(X[mask])
    print(Y[mask])

    plt.plot(X[mask], Y[mask])

    plt.show()


def test_interferogram_sample_fft():
    x, y = simulate_sample_interferogram("data/insa/001 _2_20250306T103419_spec0.txt")
    fft = FFTProcessor()

    Y = fft.fft_abs(y)

    d = 1 / 8 / len(Y)
    X = np.fft.fftshift(np.fft.fftfreq(len(Y), d))

    mask = (X >= 4000) & (X <= 12000)

    print(mask)
    print(X[mask])
    print(Y[mask])

    plt.plot(X[mask], Y[mask])

    plt.show()


def test_transmission():
    fft = FFTProcessor()

    x0, y0 = simulate_sample_interferogram("data/insa/001 _2_20250306T103419_ref.txt")
    Y0 = fft.fft_abs(y0)

    X0 = np.fft.fftshift(np.fft.fftfreq(len(Y0), 1 / 8 / len(Y0)))

    mask = (X0 >= 4000) & (X0 <= 12000)

    X01 = X0[mask]
    Y01 = Y0[mask]

    x1, y1 = simulate_sample_interferogram("data/insa/001 _2_20250306T103419_spec0.txt")
    Y1 = fft.fft_abs(y1)

    X1 = np.fft.fftshift(np.fft.fftfreq(len(Y1), 1 / 8 / len(Y1)))

    mask = (X1 >= 4000) & (X1 <= 12000)

    X11 = X1[mask]
    Y11 = Y1[mask]

    plt.plot(X01, Y01)
    plt.plot(X11, Y11)
    plt.xlim(12000, 4000)
    plt.show()

    T = Y11 / Y01
    plt.plot(X01, T)
    plt.xlim(12000, 4000)
    plt.show()

    A = np.log10(1.0 / T)
    plt.plot(X01, A)
    plt.xlim(12000, 4000)
    plt.show()
