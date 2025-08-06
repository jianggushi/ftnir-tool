import numpy as np
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QTabWidget,
    QWidget,
    QGridLayout,
    QGroupBox,
    QSpinBox,
    QDoubleSpinBox,
    QTableWidget,
    QHeaderView,
)
from PySide6.QtCore import Slot

from interfaces.qt.manager import CommManager
from model.spectrum import SpectrumData
from .interference_widget import InterferenceFigureWidget


class SignalWidget(QDialog):
    def __init__(self, comm_manager: CommManager):
        super().__init__()
        self.comm_manager = comm_manager
        self.setWindowTitle("信号检查")
        self.resize(1200, 800)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # Create three tabs
        self.tab_widget.addTab(LightStabilityWidget(self.comm_manager), "光源稳定性")
        self.create_wavelength_accuracy_tab()
        self.create_wavelength_repeatability_tab()

    def create_wavelength_accuracy_tab(self):
        """创建波长准确性标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 参数设置组
        param_group = QGroupBox("参数设置")
        param_layout = QGridLayout()
        param_group.setLayout(param_layout)

        # 参考物质选择
        param_layout.addWidget(QLabel("参考物质:"), 0, 0)
        self.accuracy_reference_combo = QComboBox()
        self.accuracy_reference_combo.addItems(
            ["聚苯乙烯薄膜", "钬玻璃", "稀土氧化物", "水蒸气"]
        )
        param_layout.addWidget(self.accuracy_reference_combo, 0, 1)

        # 标称波长
        param_layout.addWidget(QLabel("标称波长 (nm):"), 1, 0)
        self.accuracy_nominal_wavelength = QDoubleSpinBox()
        self.accuracy_nominal_wavelength.setRange(1000, 2500)
        self.accuracy_nominal_wavelength.setValue(1600)
        self.accuracy_nominal_wavelength.setDecimals(2)
        param_layout.addWidget(self.accuracy_nominal_wavelength, 1, 1)

        # 扫描次数
        param_layout.addWidget(QLabel("扫描次数:"), 2, 0)
        self.accuracy_scans_spinbox = QSpinBox()
        self.accuracy_scans_spinbox.setRange(1, 100)
        self.accuracy_scans_spinbox.setValue(16)
        param_layout.addWidget(self.accuracy_scans_spinbox, 2, 1)

        # 分辨率
        param_layout.addWidget(QLabel("分辨率 (cm⁻¹):"), 3, 0)
        self.accuracy_resolution_spinbox = QSpinBox()
        self.accuracy_resolution_spinbox.setRange(1, 32)
        self.accuracy_resolution_spinbox.setValue(4)
        param_layout.addWidget(self.accuracy_resolution_spinbox, 3, 1)

        layout.addWidget(param_group)

        # 控制按钮
        control_layout = QHBoxLayout()
        self.accuracy_start_btn = QPushButton("开始测量")
        self.accuracy_stop_btn = QPushButton("停止测量")
        self.accuracy_export_btn = QPushButton("导出数据")
        self.accuracy_stop_btn.setEnabled(False)

        control_layout.addWidget(self.accuracy_start_btn)
        control_layout.addWidget(self.accuracy_stop_btn)
        control_layout.addWidget(self.accuracy_export_btn)
        control_layout.addStretch()

        layout.addLayout(control_layout)

        # 结果显示
        result_group = QGroupBox("测量结果")
        result_layout = QVBoxLayout()
        result_group.setLayout(result_layout)

        # 统计信息
        stats_layout = QGridLayout()
        stats_layout.addWidget(QLabel("测量波长 (nm):"), 0, 0)
        self.accuracy_measured_label = QLabel("0.0")
        stats_layout.addWidget(self.accuracy_measured_label, 0, 1)

        stats_layout.addWidget(QLabel("波长误差 (nm):"), 1, 0)
        self.accuracy_error_label = QLabel("0.0")
        stats_layout.addWidget(self.accuracy_error_label, 1, 1)

        stats_layout.addWidget(QLabel("相对误差:"), 2, 0)
        self.accuracy_relative_error_label = QLabel("0.0%")
        stats_layout.addWidget(self.accuracy_relative_error_label, 2, 1)

        stats_layout.addWidget(QLabel("符合性:"), 3, 0)
        self.accuracy_compliance_label = QLabel("待测量")
        stats_layout.addWidget(self.accuracy_compliance_label, 3, 1)

        result_layout.addLayout(stats_layout)

        # 数据表格
        self.accuracy_table = QTableWidget()
        self.accuracy_table.setColumnCount(4)
        self.accuracy_table.setHorizontalHeaderLabels(
            ["标称波长", "测量波长", "误差", "状态"]
        )
        self.accuracy_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        result_layout.addWidget(self.accuracy_table)

        layout.addWidget(result_group)

        self.tab_widget.addTab(tab, "波长准确性")

    def create_wavelength_repeatability_tab(self):
        """创建波长重复性标签页"""
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)

        # 参数设置组
        param_group = QGroupBox("参数设置")
        param_layout = QGridLayout()
        param_group.setLayout(param_layout)

        # 测试波长
        param_layout.addWidget(QLabel("测试波长 (nm):"), 0, 0)
        self.repeat_wavelength_spinbox = QDoubleSpinBox()
        self.repeat_wavelength_spinbox.setRange(1000, 2500)
        self.repeat_wavelength_spinbox.setValue(1600)
        self.repeat_wavelength_spinbox.setDecimals(2)
        param_layout.addWidget(self.repeat_wavelength_spinbox, 0, 1)

        # 重复次数
        param_layout.addWidget(QLabel("重复次数:"), 1, 0)
        self.repeat_count_spinbox = QSpinBox()
        self.repeat_count_spinbox.setRange(5, 100)
        self.repeat_count_spinbox.setValue(20)
        param_layout.addWidget(self.repeat_count_spinbox, 1, 1)

        # 扫描次数
        param_layout.addWidget(QLabel("每次扫描次数:"), 2, 0)
        self.repeat_scans_spinbox = QSpinBox()
        self.repeat_scans_spinbox.setRange(1, 100)
        self.repeat_scans_spinbox.setValue(16)
        param_layout.addWidget(self.repeat_scans_spinbox, 2, 1)

        # 分辨率
        param_layout.addWidget(QLabel("分辨率 (cm⁻¹):"), 3, 0)
        self.repeat_resolution_spinbox = QSpinBox()
        self.repeat_resolution_spinbox.setRange(1, 32)
        self.repeat_resolution_spinbox.setValue(4)
        param_layout.addWidget(self.repeat_resolution_spinbox, 3, 1)

        layout.addWidget(param_group)

        # 控制按钮
        control_layout = QHBoxLayout()
        self.repeat_start_btn = QPushButton("开始测量")
        self.repeat_stop_btn = QPushButton("停止测量")
        self.repeat_export_btn = QPushButton("导出数据")
        self.repeat_stop_btn.setEnabled(False)

        control_layout.addWidget(self.repeat_start_btn)
        control_layout.addWidget(self.repeat_stop_btn)
        control_layout.addWidget(self.repeat_export_btn)
        control_layout.addStretch()

        layout.addLayout(control_layout)

        # 结果显示
        result_group = QGroupBox("测量结果")
        result_layout = QVBoxLayout()
        result_group.setLayout(result_layout)

        # 统计信息
        stats_layout = QGridLayout()
        stats_layout.addWidget(QLabel("平均波长 (nm):"), 0, 0)
        self.repeat_avg_label = QLabel("0.0")
        stats_layout.addWidget(self.repeat_avg_label, 0, 1)

        stats_layout.addWidget(QLabel("标准差 (nm):"), 1, 0)
        self.repeat_std_label = QLabel("0.0")
        stats_layout.addWidget(self.repeat_std_label, 1, 1)

        stats_layout.addWidget(QLabel("相对标准差:"), 2, 0)
        self.repeat_rsd_label = QLabel("0.0%")
        stats_layout.addWidget(self.repeat_rsd_label, 2, 1)

        stats_layout.addWidget(QLabel("最大偏差:"), 3, 0)
        self.repeat_max_dev_label = QLabel("0.0")
        stats_layout.addWidget(self.repeat_max_dev_label, 3, 1)

        result_layout.addLayout(stats_layout)

        # 数据表格
        self.repeat_table = QTableWidget()
        self.repeat_table.setColumnCount(3)
        self.repeat_table.setHorizontalHeaderLabels(["序号", "测量波长", "偏差"])
        self.repeat_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        result_layout.addWidget(self.repeat_table)

        layout.addWidget(result_group)

        self.tab_widget.addTab(tab, "波长重复性")


class LightStabilityWidget(QWidget):
    def __init__(self, comm_manager: CommManager):
        super().__init__()

        self.comm_manager = comm_manager
        self.comm_manager.light_stability_handler.add_callback(self.on_receive_data)

        self.setup_ui()
        self.setup_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        top_widget = self.create_top_widget()
        main_layout.addWidget(top_widget, 0)

        down_widget = QTabWidget()
        down_widget.addTab(self.create_chart_tab(), "图表")
        # down_widget.addTab(self.create_data_tab(), "数据")

        main_layout.addWidget(down_widget, 1)

    def setup_signals(self):
        self.start_button.clicked.connect(self.on_start)
        self.stop_button.clicked.connect(self.on_stop)

    def create_top_widget(self) -> QWidget:
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)

        top_layout.addWidget(self.create_result_group())
        top_layout.addWidget(self.create_control_group())

        return top_widget

    def create_result_group(self) -> QGroupBox:
        result_group = QGroupBox("测量结果")
        result_layout = QFormLayout()
        result_group.setLayout(result_layout)

        self.light_max_label = QLabel("0.0")
        result_layout.addRow(QLabel("最大强度:"), self.light_max_label)

        self.light_min_label = QLabel("0.0")
        result_layout.addRow(QLabel("最小强度:"), self.light_min_label)

        self.light_avg_label = QLabel("0.0")
        result_layout.addRow(QLabel("平均强度:"), self.light_avg_label)

        self.light_std_label = QLabel("0.0")
        result_layout.addRow(QLabel("标准差:"), self.light_std_label)

        return result_group

    def create_control_group(self) -> QGroupBox:
        control_group = QGroupBox("控制")
        control_layout = QVBoxLayout()
        control_group.setLayout(control_layout)

        self.start_button = QPushButton("开始测量")
        self.stop_button = QPushButton("停止测量")
        self.stop_button.setEnabled(False)

        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)

        return control_group

    def create_chart_tab(self) -> QWidget:
        chart_tab = QWidget()
        chart_layout = QVBoxLayout(chart_tab)

        self.interference_widget = InterferenceFigureWidget(self.comm_manager)

        chart_layout.addWidget(self.interference_widget)

        return chart_tab

    # def create_data_tab(self) -> QWidget:
    #     data_tab = QWidget()
    #     data_layout = QVBoxLayout(data_tab)

    #     # 数据表格
    #     self.light_table = QTableWidget()
    #     self.light_table.setColumnCount(3)
    #     self.light_table.setHorizontalHeaderLabels(["时间", "强度", "状态"])
    #     self.light_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    #     data_layout.addWidget(self.light_table)

    #     return data_tab

    def on_receive_data(self, data: SpectrumData):
        # TODO: 数据类型转换可能有问题
        interference_data = data.interference
        x_data = list(range(interference_data.shape[0]))
        self.interference_widget.update_data(x_data, interference_data.tolist())

    @Slot()
    def on_start(self):
        self.comm_manager.check_light_stability()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    @Slot()
    def on_stop(self):
        self.comm_manager.check_stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
