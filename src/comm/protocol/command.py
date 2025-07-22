import enum


class Command(enum.IntEnum):
    HANDSHAKE_REQ = 0x0101

    START_CHECK = 0x0110
    STOP_CHECK = 0x0111

    START_COLLECT = 0x10
    STOP_COLLECT = 0x11

    HANDSHAKE_RESP = 0x0201

    CHECK_RESP = 0x0210
