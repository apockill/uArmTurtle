from uf.wrapper.swift_api import SwiftAPI
from time import sleep

swift = SwiftAPI(dev_port="/dev/ttyACM0")
sleep(2)  # Give the connection time

print("Done connecting")
print("Is connected: ", swift.get_is_moving())
print("Dev info", swift.get_device_info())


swift.set_position(x=340)

sleep(10)