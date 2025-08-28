import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


def original_signal():
    # 采样点数
    N = 4096
    # 波数范围
    nu_min = 400
    nu_max = 4000
    wavenumbers = np.linspace(nu_min, nu_max, N)

    # 带吸收峰的光谱
    spectrum = np.ones(N)
    peaks = [
        (600, 20, 0.8),
        (850, 15, 0.6),
        (1100, 25, 0.9),
        (1500, 30, 0.7),
        (1750, 10, 0.5),
        (3000, 50, 0.4),
    ]
    for center, width, amplitude in peaks:
        spectrum -= amplitude * np.exp(-(((wavenumbers - center) / width) ** 2))

    interferogram = np.fft.ifft(spectrum).real

    delta_nu = (nu_max - nu_min) / (N - 1)
    opd = np.fft.fftfreq(N, delta_nu).real

    return opd, interferogram


def phase_error_signal():
    # 采样点数
    N = 4096
    # 波数范围
    nu_min = 400
    nu_max = 4000
    wavenumbers = np.linspace(nu_min, nu_max, N)

    # 带吸收峰的光谱
    spectrum = np.ones(N)
    peaks = [
        (600, 20, 0.8),
        (850, 15, 0.6),
        (1100, 25, 0.9),
        (1500, 30, 0.7),
        (1750, 10, 0.5),
        (3000, 50, 0.4),
    ]
    for center, width, amplitude in peaks:
        spectrum -= amplitude * np.exp(-(((wavenumbers - center) / width) ** 2))

    # 相位误差
    nu_center = (nu_max + nu_min) / 2.0
    a = 0.0005
    phase_error = a * (wavenumbers - nu_center)

    # 带相位误差的光谱
    complex_spectrum = spectrum * np.exp(1j * phase_error)

    interferogram = np.fft.ifft(complex_spectrum).real

    delta_nu = (nu_max - nu_min) / (N - 1)
    opd = np.fft.fftfreq(N, delta_nu)

    return opd, interferogram


def test_original_signal():
    opd, interferogram = original_signal()
    plt.plot(opd, interferogram)
    plt.show()


def test_phase_error_signal():
    opd, interferogram = original_signal()
    plt.subplot(2, 1, 1)
    plt.title("Original Signal")
    plt.plot(opd, interferogram)

    opd, interferogram = phase_error_signal()
    plt.subplot(2, 1, 2)
    plt.title("Phase Error Signal")
    plt.plot(opd, interferogram)
    plt.show()


def test_phase_error_signal_fft():
    opd, interferogram = original_signal()
    plt.subplot(2, 2, 1)
    plt.title("Original Signal")
    plt.plot(opd, interferogram)

    opd, interferogram_phase = phase_error_signal()
    plt.subplot(2, 2, 2)
    plt.title("Phase Error Signal")
    plt.plot(opd, interferogram_phase)

    spectrum = np.fft.rfft(interferogram)
    print(np.argmax(np.abs(np.real(spectrum))) / np.argmax(np.abs(np.imag(spectrum))))
    spectrum = np.abs(spectrum)
    plt.subplot(2, 2, 3)
    plt.title("Original Spectrum")
    plt.plot(spectrum)

    spectrum_phase = np.fft.rfft(interferogram_phase)
    print(
        np.argmax(np.abs(np.real(spectrum_phase)))
        / np.argmax(np.abs(np.imag(spectrum_phase)))
    )
    spectrum_phase = np.abs(spectrum_phase)
    # plt.subplot(2, 2, 4)
    plt.title("Phase Error Spectrum")
    plt.plot(spectrum_phase)

    plt.show()


# test_phase_error_signal_fft()
