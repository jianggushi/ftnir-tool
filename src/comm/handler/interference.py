import logging
import struct
import numpy as np
from typing import Callable


from .base import MessageHandler
from ..protocol.parser import RawMessage, Command

logger = logging.getLogger(__name__)


class InterferenceHandler(MessageHandler):
    def __init__(self):
        self._callbacks: list[Callable[[np.ndarray], None]] = []

    def add_callback(self, callback: Callable[[np.ndarray], None]):
        if callback not in self._callbacks:
            self._callbacks.append(callback)

    def remove_callback(self, callback: Callable[[np.ndarray], None]):
        if callback in self._callbacks:
            self._callbacks.remove(callback)

    def clear_callbacks(self):
        self._callbacks.clear()

    def handle(self, msg: RawMessage):
        if msg.command in [Command.CHECK_RESP]:
            try:
                points = self._parse_spectrum_data(msg.data)
                data = np.array(points, dtype=np.float32)
                self._run_callbacks(data)
            except Exception as e:
                logger.error(f"failed to handle message {msg.command}: {e}")

    def _run_callbacks(self, data: np.ndarray):
        for callback in self._callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"failed to run callback {callback.__name__}: {e}")

    def _parse_spectrum_data(self, data: bytes) -> list[float]:
        if len(data) % 4 != 0:
            raise ValueError(
                f"data length must be a multiple of 4, got {len(data)} bytes"
            )

        count = len(data) // 4
        return list(struct.unpack(f">{count}f", data))


import numpy as np


def generate_test_data(points=1000, cycles=10, phase=0.0):
    """生成单组正弦波数据
    Args:
        points: 数据点数 (默认1000点)
        cycles: 正弦波周期数 (默认10个周期)
        phase: 起始相位（弧度制，默认0.0）
    """
    # 时间范围根据周期数动态计算
    t = np.linspace(0, 2 * np.pi * cycles, points)

    # 添加相位偏移
    y = np.sin(t + phase)

    # 转换为大端字节序的bytes
    return struct.pack(f">{len(y)}f", *y)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    # 初始化实时绘图
    plt.ion()  # 开启交互模式
    fig, ax = plt.subplots(figsize=(12, 6))
    (line,) = ax.plot([], [], "b-")
    ax.set_title("实时光谱数据流演示", fontsize=14)
    # ax.grid(True)

    handler = InterferenceHandler()
    phase_offset = 0.0  # 初始相位

    # 模拟100次数据接收
    for _ in range(100):
        # 生成带相位偏移的测试数据（单组1000点，2个周期）
        test_bytes = generate_test_data(points=1000, cycles=20, phase=phase_offset)

        # 解析数据并添加动态相位变化
        parsed = handler._parse_spectrum_data(test_bytes)
        print(parsed)
        phase_offset += 0.1  # 每次更新相位

        # 更新绘图数据
        line.set_xdata(range(len(parsed)))
        line.set_ydata(parsed)

        # 自动调整坐标范围
        ax.relim()
        ax.autoscale_view()

        # 重绘图形
        fig.canvas.draw()
        fig.canvas.flush_events()
        # plt.pause(0.03)  # 控制刷新率约30fps

    plt.ioff()
    plt.show()
