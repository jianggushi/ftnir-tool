import enum


class Command(enum.IntEnum):
    # 握手消息
    HANDSHAKE_REQ = 0x0101
    HANDSHAKE_RES = 0x0201

    # 光源稳定性检测
    CHECK_LIGHT_STABILITY = 0x0110
    CHECK_LIGHT_STABILITY_RES = 0x0210
    # 标准物质波长准确性检测
    CHECK_STANDARD_WAVE_ACCURACY = 0x0111
    CHECK_STANDARD_WAVE_ACCURACY_RES = 0x0211
    # 标准物质波长重复性检测
    CHECK_STANDARD_WAVE_REPEATABILITY = 0x0112  # 标准物质波长重复性检测
    CHECK_STANDARD_WAVE_REPEATABILITY_RES = 0x0212
    # 停止检测
    CHECK_STOP = 0x011F

    START_COLLECT = 0x10
    STOP_COLLECT = 0x11

    # 打开光源
    TURN_ON_LIGHT = 0x0301
    # 关闭光源
    TURN_OFF_LIGHT = 0x0302
    # 打开激光
    TURN_ON_LASER = 0x0303
    # 关闭激光
    TURN_OFF_LASER = 0x0304

    # 设置旋转电机偏移量
    SET_ROTATE_OFFSET = 0x0310
    # 设置旋转电机目标位置
    SET_ROTATE_TARGET = 0x0311

    # 设置丝杆电机偏移量
    SET_SCREW_OFFSET = 0x0312
    # 设置丝杆电机目标位置
    SET_SCREW_TARGET = 0x0313
