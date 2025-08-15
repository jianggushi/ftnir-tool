import logging
import struct
import numpy as np
from collections import deque

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager
from core.model.spectrum import SpectrumData
from core.processor.interference import FFTProcessor

from .base import BaseService, parse_interference_data


logger = logging.getLogger(__name__)


class CollectService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager
        self._fft_processor = FFTProcessor()

    def handle(self, msg: RawMessage):
        if (
            msg.command != Command.COLLECT_DARK_NOISE_RES
            and msg.command != Command.COLLECT_BACKGROUND_RES
            and msg.command != Command.COLLECT_SAMPLE_RES
        ):
            return
        try:
            points = parse_interference_data(msg.data)
            interference_data = np.array(points, dtype=np.float32)

            spectrum_data = self._fft_processor.process(interference_data)

            # save data
            # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
            # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

            # run callbacks
            spectrum_data = SpectrumData(
                interference_data,
                spectrum_data,
            )
            self._run_callbacks(spectrum_data)
        except Exception as e:
            logger.error(f"failed to handle message {msg.command}: {e}")

    # def handle_dark_noise_res(self, msg: RawMessage):
    #     if msg.command != Command.COLLECT_DARK_NOISE_RES:
    #         return
    #     try:
    #         points = self._parse_spectrum_data(msg.data)
    #         interference_data = np.array(points, dtype=np.float32)

    #         spectrum_data = self._fft_processor.process(interference_data)

    #         # # save data
    #         # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    #         # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

    #         # run callbacks
    #         spectrum_data = SpectrumData(interference_data, spectrum_data)
    #         self._run_callbacks(spectrum_data)
    #     except Exception as e:
    #         logger.error(f"failed to handle message {msg.command}: {e}")

    # def handle_background_res(self, msg: RawMessage):
    #     if msg.command != Command.COLLECT_BACKGROUND_RES:
    #         return
    #     try:
    #         points = self._parse_spectrum_data(msg.data)
    #         interference_data = np.array(points, dtype=np.float32)

    #         spectrum_data = self._fft_processor.process(interference_data)

    #         # # save data
    #         # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    #         # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

    #         # run callbacks
    #         spectrum_data = SpectrumData(interference_data, spectrum_data)
    #         self._run_callbacks(spectrum_data)
    #     except Exception as e:
    #         logger.error(f"failed to handle message {msg.command}: {e}")

    # def handle_sample_res(self, msg: RawMessage):

    #     if msg.command != Command.COLLECT_SAMPLE_RES:
    #         return
    #     try:
    #         points = self._parse_spectrum_data(msg.data)
    #         interference_data = np.array(points, dtype=np.float32)

    #         spectrum_data = self._fft_processor.process(interference_data)

    #         # # save data
    #         # filename = f"data/interference_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    #         # np.savetxt(filename, interference_data, fmt="%.6f", delimiter=",")

    #         # run callbacks
    #         spectrum_data = SpectrumData(interference_data, spectrum_data)
    #         self._run_callbacks(spectrum_data)
    #     except Exception as e:
    #         logger.error(f"failed to handle message {msg.command}: {e}")

    def collect_dark_noise(self, num: int, continuous_mode: bool):
        """采集暗噪声"""
        if continuous_mode:
            self.comm_manager.send_message(
                Command.COLLECT_DARK_NOISE_REQ, struct.pack(">B", 0xFF)
            )
        else:
            data = struct.pack(">B", 0x01) + struct.pack(">H", num)
            self.comm_manager.send_message(Command.COLLECT_DARK_NOISE_REQ, data)

    def collect_background(self, num: int, continuous_mode: bool):
        """采集背景"""
        if continuous_mode:
            self.comm_manager.send_message(
                Command.COLLECT_BACKGROUND_REQ, struct.pack(">B", 0xFF)
            )
        else:
            data = struct.pack(">B", 0x01) + struct.pack(">H", num)
            self.comm_manager.send_message(Command.COLLECT_BACKGROUND_REQ, data)

    def collect_sample(self, num: int, continuous_mode: bool):
        """采集样本"""
        if continuous_mode:
            self.comm_manager.send_message(
                Command.COLLECT_SAMPLE_REQ, struct.pack(">B", 0xFF)
            )
        else:
            data = struct.pack(">B", 0x01) + struct.pack(">H", num)
            self.comm_manager.send_message(Command.COLLECT_SAMPLE_REQ, data)

    def stop_collect(self):
        """停止采集"""
        self.comm_manager.send_message(Command.COLLECT_STOP_REQ)
