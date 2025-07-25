import serial
import time


def test_serial_open():
    ser = serial.Serial(
        port="COM1",
        baudrate=115200,
        bytesize=8,
        stopbits=1,
        parity="N",
    )
    assert ser.is_open, "Serial port should be open"

    ser.write(b"Hello Serial Port")
    time.sleep(60)  # Keep the port open for 60 seconds


def test_serial_write():
    ser = serial.Serial(
        port="COM1",
        baudrate=115200,
        bytesize=8,
        stopbits=1,
        parity="N",
    )
    assert ser.is_open, "Serial port should be open"

    test_data = b"A" * 40000
    n = ser.write(test_data)
    print(f"Wrote {n} bytes to serial port")
    time.sleep(1)  # Wait for the data to be sent
    ser.close()
    assert not ser.is_open, "Serial port should be closed after write"


if __name__ == "__main__":
    test_serial_write()
