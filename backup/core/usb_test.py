# import libusb_package
# from usb.core import Device
# import usb.util
# from typing import Optional
# import logging

# VENDOR_ID: int = 0x0BDA
# PRODUCT_ID: int = 0x8152

# device: Device= libusb_package.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
# print(device)
# print(device.configurations())
# for cfg in device:
#     print(cfg.bConfigurationValue)
#     print(cfg)

# device.set_configuration(1)
# cfg = device.get_active_configuration()
# # print(cfg)

# # intf = cfg

# data = device.read(0x83, 10, 3000)
# print(data)

# # while True:
# #     try:
# #         data = device.read(0x83, 10)
# #         print(data)
# #     except Exception as e:
# #         continue


# #   timeout = 10000
# #         buffer = bytearray()
# #         endpoint = self.device[0][(0,0)][0]
# #         # if self.device.is_kernel_driver_active(0):
# #         #     self.device.detach_kernel_driver(0)
# #             # self.device.claim_interface(0)
# #         while True:
# #             try:
# #                 data = self.device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSizet)
# #                 print(data)
# #                 buffer.extend(data)
# #             except Exception as e:
# #                 continue
# #         return buffer
