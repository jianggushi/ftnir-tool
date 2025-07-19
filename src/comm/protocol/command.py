import enum


class Command(enum.IntEnum):
    HANDSHAKE = 0x01

    START_COLLECT = 0x10
    STOP_COLLECT = 0x11

    START_CHECK = 0x20
    STOP_CHECK = 0x21

    CHECK_RESULT = 0x80
