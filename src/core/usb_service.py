import libusb_package
from usb.core import Device
from typing import Optional
import logging

VENDOR_ID: int = 0x0BDA
PRODUCT_ID: int = 0x8152

class UsbService():
    def __init__(self):
        self.device: Device = None
        
    def find_device(self) -> Optional[Device]:
        dev: Optional[Device] = libusb_package.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        # was it found?
        if dev is None:
            logging.error("Device not found")
        return dev
    
    def connect_device(self, device_obj: Device):
        if device_obj is None:
            logging.error("Device is None")
            return
        
        if self.device:
            return
        self.device = device_obj
        
        try:
            self.device.set_configuration()
            cfg = self.device.get_active_configuration()
            print(cfg)
        except Exception as e:
            logging.exception(f"Device configuration failed: {e}")
    
    def read_data(self) -> bytearray:
        timeout = 10000
        buffer = bytearray()
        endpoint = self.device[0][(0,0)][0]
        # if self.device.is_kernel_driver_active(0):
        #     self.device.detach_kernel_driver(0)
            # self.device.claim_interface(0)
        while True:
            try:
                data = self.device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSizet)
                print(data)
                buffer.extend(data)
            except Exception as e:
                continue
        return buffer

if __name__=="__main__":
    usb_service = UsbService()
    device = usb_service.find_device()
    print(device)
    usb_service.connect_device(device)
    data = usb_service.read_data()