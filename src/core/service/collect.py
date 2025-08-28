import logging
import struct
import time
import numpy as np

from comm.protocol.parser import RawMessage, Command
from comm.manager import CommManager
from config.types import CollectData
from core.processor.interference import FFTProcessor
from core.store.txt import TxtStore

from .base import BaseService, parse_interference_data
from .instrument_info import instrumentInfo

logger = logging.getLogger(__name__)


class CollectService(BaseService):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager
        self._fft_processor = FFTProcessor()
        self.instrumentInfo = instrumentInfo

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

            d = (
                1.0
                / self.instrumentInfo.get_resolution().to_float()
                / len(spectrum_data)
            )

            freq_data = self._fft_processor.fft_freq(len(spectrum_data), d)

            # mask = (freq_data >= 4000) & (freq_data <= 12000)
            mask = freq_data >= 4000
            freq_data = freq_data[mask]
            spectrum_data = spectrum_data[mask]

            # save data
            now = time.strftime("%Y%m%d_%H%M%S")
            filename = f"data/interference_{now}.txt"
            meta_data = {
                "Time": now,
                "Direction": "Positive",
                "Lamp current": 0.0,
                "Interferometer temperature": 0.0,
                "Interferometer humidity": 0.0,
                "Laser wavelength(nm)": 638.0,
                "VCM speed": 0.0,
                "Resolution": 8,
                "Gain": 1,
                "Acquisition Times": 1,
            }
            TxtStore().write(filename, interference_data, meta=meta_data)

            # run callbacks
            spectrum_data = CollectData(
                interference_data,
                freq_data,
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
