import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def original_signal():
    x = np.linspace(0, 1, 100)
    y = np.cos(2 * np.pi * 5.3 * x)
    return x, y


def test_rectangle_window():
    """
    测试矩形窗口
    """
    plt.figure(figsize=(10, 8))

    x, y = original_signal()

    plt.subplot(3, 2, 1)
    plt.title("Original Signal")
    plt.plot(x, y)

    y_fft = np.abs(np.fft.rfft(y))
    plt.subplot(3, 2, 2)
    plt.title("FFT of Original")
    plt.plot(y_fft)

    window = signal.get_window("boxcar", len(y))
    plt.subplot(3, 2, 3)
    plt.title("Rectangle Window")
    plt.plot(window)

    window_fft = np.abs(np.fft.rfft(window))
    plt.subplot(3, 2, 4)
    plt.title("FFT of Window")
    plt.plot(window_fft)

    y_window = y * window
    plt.subplot(3, 2, 5)
    plt.title("Original Signal VS Windowed Singal")
    plt.plot(x, y, label="Original Signal")
    plt.plot(x, y_window, label="Windowed Signal")
    plt.legend()

    y_window_fft = np.abs(np.fft.rfft(y_window))
    plt.subplot(3, 2, 6)
    plt.title("FFT of Windowed Signal")
    plt.plot(y_window_fft)

    plt.show()


def test_triangle_window():
    """
    测试三角窗口
    """
    plt.figure(figsize=(10, 8))

    x, y = original_signal()

    plt.subplot(3, 2, 1)
    plt.title("Original Signal")
    plt.plot(x, y)

    y_fft = np.abs(np.fft.rfft(y))
    plt.subplot(3, 2, 2)
    plt.title("FFT of Original")
    plt.plot(y_fft)

    window = signal.get_window("triang", len(y))
    plt.subplot(3, 2, 3)
    plt.title("Triangle Window")
    plt.plot(window)

    window_fft = np.abs(np.fft.rfft(window))
    plt.subplot(3, 2, 4)
    plt.title("FFT of Window")
    plt.plot(window_fft)

    y_window = y * window
    plt.subplot(3, 2, 5)
    plt.title("Original Signal VS Windowed Singal")
    plt.plot(x, y, label="Original Signal")
    plt.plot(x, y_window, label="Windowed Signal")
    plt.legend()

    y_window_fft = np.abs(np.fft.rfft(y_window))
    plt.subplot(3, 2, 6)
    plt.title("FFT of Windowed Signal")
    plt.plot(y_window_fft)

    plt.show()


def test_gaussian_window():
    """
    测试高斯窗口
    """
    plt.figure(figsize=(10, 8))

    x, y = original_signal()

    plt.subplot(3, 2, 1)
    plt.title("Original Signal")
    plt.plot(x, y)

    y_fft = np.abs(np.fft.rfft(y))
    plt.subplot(3, 2, 2)
    plt.title("FFT of Original")
    plt.plot(y_fft)

    window = signal.get_window(("gaussian", len(y) / 8), len(y))
    plt.subplot(3, 2, 3)
    plt.title("Gaussian Window")
    plt.plot(window)

    window_fft = np.abs(np.fft.rfft(window))
    plt.subplot(3, 2, 4)
    plt.title("FFT of Window")
    plt.plot(window_fft)

    y_window = y * window
    plt.subplot(3, 2, 5)
    plt.title("Original Signal VS Windowed Singal")
    plt.plot(x, y, label="Original Signal")
    plt.plot(x, y_window, label="Windowed Signal")
    plt.legend()

    y_window_fft = np.abs(np.fft.rfft(y_window))
    plt.subplot(3, 2, 6)
    plt.title("FFT of Windowed Signal")
    plt.plot(y_window_fft)

    plt.show()


def test_hamming_window():
    """
    测试汉明窗口
    """
    plt.figure(figsize=(10, 8))

    x, y = original_signal()

    plt.subplot(3, 2, 1)
    plt.title("Original Signal")
    plt.plot(x, y)

    y_fft = np.abs(np.fft.rfft(y))
    plt.subplot(3, 2, 2)
    plt.title("FFT of Original")
    plt.plot(y_fft)

    window = signal.get_window("hamming", len(y))
    plt.subplot(3, 2, 3)
    plt.title("Hamming Window")
    plt.plot(window)

    window_fft = np.abs(np.fft.rfft(window))
    plt.subplot(3, 2, 4)
    plt.title("FFT of Window")
    plt.plot(window_fft)

    y_window = y * window
    plt.subplot(3, 2, 5)
    plt.title("Original Signal VS Windowed Singal")
    plt.plot(x, y, label="Original Signal")
    plt.plot(x, y_window, label="Windowed Signal")
    plt.legend()

    y_window_fft = np.abs(np.fft.rfft(y_window))
    plt.subplot(3, 2, 6)
    plt.title("FFT of Windowed Signal")
    plt.plot(y_window_fft)

    plt.show()


def test_hann_window():
    """
    测试汉宁窗口
    """
    plt.figure(figsize=(10, 8))

    x, y = original_signal()

    plt.subplot(3, 2, 1)
    plt.title("Original Signal")
    plt.plot(x, y)

    y_fft = np.abs(np.fft.rfft(y))
    plt.subplot(3, 2, 2)
    plt.title("FFT of Original")
    plt.plot(y_fft)

    window = signal.get_window("hann", len(y))
    plt.subplot(3, 2, 3)
    plt.title("Hann Window")
    plt.plot(window)

    window_fft = np.abs(np.fft.rfft(window))
    plt.subplot(3, 2, 4)
    plt.title("FFT of Window")
    plt.plot(window_fft)

    y_window = y * window
    plt.subplot(3, 2, 5)
    plt.title("Original Signal VS Windowed Singal")
    plt.plot(x, y, label="Original Signal")
    plt.plot(x, y_window, label="Windowed Signal")
    plt.legend()

    y_window_fft = np.abs(np.fft.rfft(y_window))
    plt.subplot(3, 2, 6)
    plt.title("FFT of Windowed Signal")
    plt.plot(y_window_fft)

    plt.show()


def test_blackmanharris_window():
    """
    测试布莱克曼Harris窗口
    """
    plt.figure(figsize=(10, 8))

    x, y = original_signal()

    plt.subplot(3, 2, 1)
    plt.title("Original Signal")
    plt.plot(x, y)

    y_fft = np.abs(np.fft.rfft(y))
    plt.subplot(3, 2, 2)
    plt.title("FFT of Original")
    plt.plot(y_fft)

    window = signal.get_window("blackmanharris", len(y))
    plt.subplot(3, 2, 3)
    plt.title("BlackmanHarris Window")
    plt.plot(window)

    window_fft = np.abs(np.fft.rfft(window))
    plt.subplot(3, 2, 4)
    plt.title("FFT of Window")
    plt.plot(window_fft)

    y_window = y * window
    plt.subplot(3, 2, 5)
    plt.title("Original Signal VS Windowed Singal")
    plt.plot(x, y, label="Original Signal")
    plt.plot(x, y_window, label="Windowed Signal")
    plt.legend()

    y_window_fft = np.abs(np.fft.rfft(y_window))
    plt.subplot(3, 2, 6)
    plt.title("FFT of Windowed Signal")
    plt.plot(y_window_fft)

    plt.show()
