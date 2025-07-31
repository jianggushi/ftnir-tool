from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QRadioButton,
    QTabWidget,
    QWidget,
    QGridLayout,
    QTextEdit,
    QGroupBox,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QSplitter,
)
from PySide6.QtCore import Qt
from handler.manager import CommManager
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
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # splitter = QSplitter(Qt.Orientation.Vertical)
        # layout.addWidget(splitter)

        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)

        # Create and add parameter, control, and result groups
        top_layout.addWidget(self.create_param_group())
        top_layout.addWidget(self.create_result_group())
        top_layout.addWidget(self.create_control_group())

        layout.addWidget(top_widget, 0)

        down_widget = QTabWidget()
        down_widget.addTab(self.create_chart_tab(), "图表")
        down_widget.addTab(self.create_data_tab(), "数据")

        layout.addWidget(down_widget, 1)

        # splitter.setSizes([200, 600])  # Set initial sizes for the splitter

        # Set the layout for this widget
        self.setLayout(layout)

    def create_param_group(self) -> QGroupBox:
        param_group = QGroupBox("参数设置")
        param_layout = QFormLayout()
        param_group.setLayout(param_layout)

        # 测量时间
        self.light_time_spinbox = QSpinBox()
        self.light_time_spinbox.setRange(1, 3600)
        self.light_time_spinbox.setValue(60)
        param_layout.addRow(QLabel("测量时间 (秒):"), self.light_time_spinbox)

        # 采样间隔
        self.light_interval_spinbox = QSpinBox()
        self.light_interval_spinbox.setRange(1, 60)
        self.light_interval_spinbox.setValue(5)
        param_layout.addRow(QLabel("采样间隔 (秒):"), self.light_interval_spinbox)

        return param_group

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

        self.light_start_btn = QPushButton("开始测量")
        self.light_stop_btn = QPushButton("停止测量")
        self.light_stop_btn.setEnabled(False)

        control_layout.addWidget(self.light_start_btn)
        control_layout.addWidget(self.light_stop_btn)
        control_layout.addStretch()

        return control_group

    def create_chart_tab(self) -> QWidget:
        chart_tab = QWidget()
        chart_layout = QVBoxLayout(chart_tab)

        chart_layout.addWidget(InterferenceFigureWidget(self.comm_manager))

        return chart_tab

    def create_data_tab(self) -> QWidget:
        data_tab = QWidget()
        data_layout = QVBoxLayout(data_tab)

        # 数据表格
        self.light_table = QTableWidget()
        self.light_table.setColumnCount(3)
        self.light_table.setHorizontalHeaderLabels(["时间", "强度", "状态"])
        self.light_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        data_layout.addWidget(self.light_table)

        return data_tab
