import pytest
import time

from comm.transport.serial import SerialTransport


def print_data(data: bytes):
    print(data.hex(), flush=True)


def test_send_data():
    transport = SerialTransport("COM1")
    transport.open()
    transport.send_data(b"\x01\x02\x03\x04\x05")

    # while True:
    #     data = transport.receive_data()
    #     print(data.hex(), flush=True)
    #     time.sleep(0.1)

    transport.on_data_received(print_data)

    input("按回车退出程序\n")

    transport.close()
    # time.sleep(1000000)


if __name__ == "__main__":
    test_send_data()
