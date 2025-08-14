import threading
import logging
import struct
from PySide6.QtCore import Signal, QObject


from comm.transport.serial import SerialTransport
from comm.protocol.parser import MessageParser
from comm.protocol.parser import RawMessage
from comm.protocol.parser import Command

from core.service.base import MessageHandler
from core.service.light_stablity import LightStabilityHandler
from core.service.interference import DarkNoiseHandler
from core.service.interference import BackgroundHandler
from core.service.interference import SampleHandler

from .handshake import HandshakeControler
from .message import MessageSender


logger = logging.getLogger(__name__)


class QtController(QObject):
    status_bar_updated = Signal(str, object)

    def __init__(self):
        QObject.__init__(self)

        self.transport = SerialTransport()
        self.transport.on_data_received(self._handle_raw_data)

        self.message_sender = MessageSender(self.transport)

        self._parser = MessageParser()
        self._lock = threading.Lock()

        self._connected = False
        self._handshake = HandshakeControler(self.message_sender)

        self.light_stability_handler = LightStabilityHandler()
        self.dark_noise_handler = DarkNoiseHandler()
        self.background_handler = BackgroundHandler()
        self.sample_handler = SampleHandler()

        self._message_handlers: dict[Command, MessageHandler] = {
            Command.HANDSHAKE_REQ: self._handshake,
            Command.HANDSHAKE_RES: self._handshake,
            Command.CHECK_LIGHT_STABILITY_RES: self.light_stability_handler,
            Command.COLLECT_DARK_NOISE_RES: self.dark_noise_handler,
            Command.COLLECT_BACKGROUND_RES: self.background_handler,
            Command.COLLECT_SAMPLE_RES: self.sample_handler,
        }

    def connect(self, **kwargs):
        try:
            if not self.transport.is_open:
                port = kwargs.get("port", "")
                self.transport.set_port(port)
                self.transport.open()
                self._connected = True
                self.status_bar_updated.emit("transport", "已打开")

            # 开始握手
            self._handshake.start()
        except Exception as e:
            logger.error(f"连接失败: {e}")
            self.status_bar_updated.emit("transport", "错误")
            self.disconnect()

    def disconnect(self):
        self._connected = False
        self._handshake.stop()
        logger.info("stoped handshake")
        if self.transport.is_open:
            self.transport.close()
            self.status_bar_updated.emit("transport", "关闭")

    def list_ports(self) -> list[str]:
        return self.transport.list_ports()

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _handle_raw_data(self, data: bytes):
        with self._lock:
            self._parser.feed(data)
            for raw_message in self._parser.parse():
                self._process_message(raw_message)

    def _process_message(self, msg: RawMessage):
        """处理接收到的消息"""
        logger.info(
            f"received message: {msg.command.name}, payload length: {len(msg.data)}"
        )
        handler = self._message_handlers.get(msg.command)
        if handler:
            handler.handle(msg)
        else:
            logger.warning(f"no handler found for message: {msg.command.name}")

    def _send_message(self, command: Command, data: bytes = b""):
        self.message_sender.send_message(command, data)

    def register_handler(self, command: Command, handler: MessageHandler):
        """注册消息处理器"""
        self._message_handlers[command] = handler

    def unregister_handler(self, command: Command):
        """注销消息处理器"""
        if command in self._message_handlers:
            del self._message_handlers[command]

    def start_collect(self):
        self._send_message(Command.START_COLLECT)

    def stop_collect(self):
        self._send_message(Command.STOP_COLLECT)

    def check_light_stability(self):
        self._send_message(Command.CHECK_LIGHT_STABILITY, b"\01")

    def check_standard_wave_accuracy(self):
        self._send_message(Command.CHECK_STANDARD_WAVE_ACCURACY, b"\02")

    def check_standard_wave_repeatability(self):
        self._send_message(Command.CHECK_STANDARD_WAVE_REPEATABILITY, b"\03")

    def check_stop(self):
        self._send_message(Command.CHECK_STOP, b"\03")

    def turn_on_light(self):
        self._send_message(Command.TURN_ON_LIGHT)

    def turn_off_light(self):
        self._send_message(Command.TURN_OFF_LIGHT)

    def turn_on_laser(self):
        self._send_message(Command.TURN_ON_LASER)

    def turn_off_laser(self):
        self._send_message(Command.TURN_OFF_LASER)

    def set_rotate_offset(self, offset: int):
        self._send_message(Command.SET_ROTATE_OFFSET, struct.pack(">H", offset))

    def set_rotate_target(self, target: int):
        self._send_message(Command.SET_ROTATE_TARGET, struct.pack(">B", target))

    def set_screw_offset(self, offset: int):

        self._send_message(Command.SET_SCREW_OFFSET, struct.pack(">H", offset))

    def set_screw_target(self, target: int):
        self._send_message(Command.SET_SCREW_TARGET, struct.pack(">B", target))

    def set_hardware_setting(self, setting: int):
        self._send_message(Command.SET_HARDWARE_SETTING, struct.pack(">B", setting))

    def collect_dark_noise(self, num: int, continuous_mode: bool):
        """采集暗噪声"""
        if continuous_mode:
            self._send_message(Command.COLLECT_DARK_NOISE_REQ, struct.pack(">B", 0xFF))
        else:
            data = struct.pack(">B", 0x01) + struct.pack(">H", num)
            self._send_message(Command.COLLECT_DARK_NOISE_REQ, data)

    def collect_background(self, num: int, continuous_mode: bool):
        """采集背景"""
        if continuous_mode:
            self._send_message(Command.COLLECT_BACKGROUND_REQ, struct.pack(">B", 0xFF))
        else:
            data = struct.pack(">B", 0x01) + struct.pack(">H", num)
            self._send_message(Command.COLLECT_BACKGROUND_REQ, data)

    def collect_sample(self, num: int, continuous_mode: bool):
        """采集样本"""
        if continuous_mode:
            self._send_message(Command.COLLECT_SAMPLE_REQ, struct.pack(">B", 0xFF))
        else:
            data = struct.pack(">B", 0x01) + struct.pack(">H", num)
            self._send_message(Command.COLLECT_SAMPLE_REQ, data)

    def collect_stop(self):
        """停止采集"""
        self._send_message(Command.COLLECT_STOP_REQ)

    # def save_light_stability_data(self, data: LightStability):
    #     with db.session() as session:
    #         session.add(data)
    #         session.commit()
