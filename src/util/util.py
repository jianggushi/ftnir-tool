from matplotlib import rcParams


def init_font():
    rcParams["font.family"] = ["Microsoft YaHei", "SimHei"]
    rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
