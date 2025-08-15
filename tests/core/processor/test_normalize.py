import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

t = np.linspace(-0.5, 0.5, 21)  # 时间轴
x = np.sin(np.pi * t) + 1 / 4  # 正弦信号+直流分量

x_detrend = signal.detrend(x, type="constant")

ax = plt.subplot()
ax.axhline(0, color="black", linewidth=0.5)
ax.axvline(0, color="black", linewidth=0.5)

ax.plot(t, x, label="x")
ax.plot(t, x_detrend, label="x_detrend")


ax.legend()
plt.show()
