import libusb_package
import usb.core
from usb.core import Device
from typing import Optional
import logging

# 设置你的设备的 VID 和 PID（需要替换为你的实际值）
# VENDOR_ID: int = 0x0951
# PRODUCT_ID: int = 0x1666

VENDOR_ID: int = 0x17ef
PRODUCT_ID: int = 0x6099

def find_device() -> Optional[Device]:
    try:
        # find our device
        dev: Optional[Device] = libusb_package.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        # was it found?
        if dev is None:
            logging.error("Device not found")
            return None
        cfg = dev.get_active_configuration()
        # print(cfg)
        if cfg is None:
            dev.set_configuration()
        return dev
    except Exception as e:
        logging.exception(f"Device configuration failed: {e}")

def read_data(dev: Device):
    dev.read(0x81, 64, 3000)
    pass

dev = find_device()
print(dev)