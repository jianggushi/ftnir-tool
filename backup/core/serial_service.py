import serial
import time

ser = serial.Serial("COM1")

print(ser.name)
ser.write(b'hello')

time.sleep(60)
ser.close()