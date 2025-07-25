from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PySide6.QtCore import Slot

from comm.manager import CommManager
from comm.protocol.command import Command

from .communication_widget import CommunicationWidget
from .signal_widget import SignalCheckWidget
from .collect_widget import CollectWidget


class ControlWidget(QWidget):
    def __init__(self, comm_manager: CommManager):
        super().__init__()
        self.setup_ui()

        self.comm_manager = comm_manager

    def setup_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Add communication widget
        self.comm_widget = CommunicationWidget()
        self.comm_widget.connected.connect(self.on_connect)
        self.comm_widget.disconnected.connect(self.on_disconnect)

        # Add signal check widget
        self.signal_widget = SignalCheckWidget()
        self.signal_widget.check_started.connect(self.on_check_start)
        self.signal_widget.check_stopped.connect(self.on_check_stop)

        # Add collect widget
        self.collect_widget = CollectWidget()
        self.collect_widget.data_collected.connect(
            self.on_data_collected
        )  # 连接采集数据信号

        # Add widgets to main layout
        main_layout.addWidget(self.comm_widget)
        main_layout.addWidget(self.signal_widget)
        main_layout.addWidget(self.collect_widget)
        main_layout.addStretch()

    @Slot()
    def on_connect(self):
        # Handle connection event
        self.comm_manager.connect()

    @Slot()
    def on_disconnect(self):
        # Handle disconnection event
        self.comm_manager.disconnect()

    @Slot()
    def on_check_start(self, check_type: str):
        """开始信号检查"""
        # 根据检查类型发送不同的命令
        if check_type == "光源稳定性":
            self.comm_manager.start_check_stability()
        elif check_type == "波长准确性":
            self.comm_manager.start_check_accuracy()
        elif check_type == "波长重复性":
            self.comm_manager.start_check_repeatability()
        else:
            raise ValueError(f"未知检查类型: {check_type}")

    @Slot()
    def on_check_stop(self):
        """停止信号检查"""
        if self.signal_widget.stability_radio.isChecked():
            self.comm_manager.stop_check_stability()
        elif self.signal_widget.accuracy_radio.isChecked():
            self.comm_manager.stop_check_accuracy()
        elif self.signal_widget.repeatability_radio.isChecked():
            self.comm_manager.stop_check_repeatability()
        else:
            raise ValueError("没有选中的检查类型")

    @Slot(list, list)
    def on_data_collected(self, x_data, y_data):
        """处理采集到的数据并更新图表"""
        self.figure_widget.update_data(x_data, y_data)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    from config.log import setup_logging

    setup_logging()

    app = QApplication(sys.argv)
    comm_manager = CommManager()  # 创建 CommManager 实例
    widget = ControlWidget(comm_manager=comm_manager)
    widget.show()
    app.exit(app.exec())
