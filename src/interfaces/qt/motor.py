import logging

from PySide6.QtCore import QObject, Signal

from core.service.motor import RotateMotorService
from core.service.motor import ScrewMotorService
from ui_qt.control_widget import RotateMotorWidget
from ui_qt.control_widget import ScrewMotorWidget

logger = logging.getLogger(__name__)


class RotateMotorController(QObject):
    def __init__(
        self,
        svc: RotateMotorService,
        view: RotateMotorWidget,
    ):
        super().__init__()

        self.svc = svc
        self.view = view

        self.view.offset_button.clicked.connect(self.on_offset_set)
        self.view.target_1_button.clicked.connect(self.on_target_1_set)
        self.view.target_2_button.clicked.connect(self.on_target_2_set)
        self.view.target_3_button.clicked.connect(self.on_target_3_set)
        self.view.target_4_button.clicked.connect(self.on_target_4_set)
        self.view.target_5_button.clicked.connect(self.on_target_5_set)
        self.view.target_6_button.clicked.connect(self.on_target_6_set)
        self.view.target_reset_button.clicked.connect(self.on_target_reset)

    def on_offset_set(self):
        try:
            offset = self.view.get_offset()
            self.svc.set_rotate_offset(offset)
        except Exception as e:
            logger.error(f"设置旋转电机偏移量失败: {e}")

    def on_target_1_set(self):
        try:
            self.svc.set_rotate_target(1)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_2_set(self):
        try:
            self.svc.set_rotate_target(2)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_3_set(self):
        try:
            self.svc.set_rotate_target(3)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_4_set(self):
        try:
            self.svc.set_rotate_target(4)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_5_set(self):
        try:
            self.svc.set_rotate_target(5)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_6_set(self):
        try:
            self.svc.set_rotate_target(6)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_reset(self):
        try:
            self.svc.set_rotate_target(0)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")


class ScrewMotorController(QObject):
    def __init__(
        self,
        svc: ScrewMotorService,
        view: ScrewMotorWidget,
    ):
        super().__init__()

        self.svc = svc
        self.view = view

        self.view.offset_button.clicked.connect(self.on_offset_set)
        self.view.target_1_button.clicked.connect(self.on_target_1_set)
        self.view.target_2_button.clicked.connect(self.on_target_2_set)
        self.view.target_3_button.clicked.connect(self.on_target_3_set)
        self.view.target_4_button.clicked.connect(self.on_target_4_set)
        self.view.target_5_button.clicked.connect(self.on_target_5_set)
        self.view.target_6_button.clicked.connect(self.on_target_6_set)
        self.view.target_7_button.clicked.connect(self.on_target_7_set)
        self.view.target_8_button.clicked.connect(self.on_target_8_set)
        self.view.target_reset_button.clicked.connect(self.on_target_reset)
        self.view.target_hide_button.clicked.connect(self.on_target_hide)

    def on_offset_set(self):
        try:
            offset = self.view.get_offset()
            self.svc.set_screw_offset(offset)
        except Exception as e:
            logger.error(f"设置旋转电机偏移量失败: {e}")

    def on_target_1_set(self):
        try:
            self.svc.set_screw_target(1)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_2_set(self):
        try:
            self.svc.set_screw_target(2)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_3_set(self):
        try:
            self.svc.set_screw_target(3)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_4_set(self):
        try:
            self.svc.set_screw_target(4)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_5_set(self):
        try:
            self.svc.set_screw_target(5)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_6_set(self):
        try:
            self.svc.set_screw_target(6)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_7_set(self):
        try:
            self.svc.set_screw_target(7)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_8_set(self):
        try:
            self.svc.set_screw_target(8)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_reset(self):
        try:
            self.svc.set_screw_target(0)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")

    def on_target_hide(self):
        try:
            self.svc.set_screw_target(9)
        except Exception as e:
            logger.error(f"设置旋转电机目标位置失败: {e}")
