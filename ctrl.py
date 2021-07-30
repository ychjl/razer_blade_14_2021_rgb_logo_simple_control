import argparse
import usb.core
import usb.util
from functools import reduce
# parse args
parser = argparse.ArgumentParser(description = "simple rgb/logo controller for razer blade 14 2021; use with sudo")
parser.add_argument("--logo", "-l", type = int, help = "0 for off, 1 for static and 2 for breathing")
parser.add_argument("--rgb", "-r", type = int, nargs = 3, help = "rgb decimal ints(0-255): 11 22 33 for example")
parser.add_argument("--default", "-d", action = "count", default = 0, help = "perform default action: 0 and 2 2 2")
args = parser.parse_args()
if args.default > 0:
    if args.logo is None:
        args.logo = 0
    if args.rgb is None:
        args.rgb = [2, 2, 2]

# setup usb device
dev = usb.core.find(idVendor = 0x1532, idProduct = 0x0270)
if dev.is_kernel_driver_active(2):
    dev.detach_kernel_driver(2)
usb.util.claim_interface(dev, 2)

# configure logo
logo_msg = {
    0 : [b"\x00\x1F\x00\x00\x00\x03\x03\x03\x01\x05\xFF" + b"\x00"*77 + b"\xF8\x00", b"\x00\x1F\x00\x00\x00\x03\x03\x00\x01\x04\x00" + b"\x00"*77 + b"\x05\x00"],
    1 : [b"\x00\x1F\x00\x00\x00\x03\x03\x03\x01\x05\xFF" + b"\x00"*77 + b"\xF8\x00", b"\x00\x1F\x00\x00\x00\x03\x03\x02\x01\x04\x00" + b"\x00"*77 + b"\x07\x00", b"\x00\x1F\x00\x00\x00\x03\x03\x00\x01\x04\x01" + b"\x00"*77 + b"\x04\x00"],
    2 : [b"\x00\x1F\x00\x00\x00\x03\x03\x03\x01\x05\xFF" + b"\x00"*77 + b"\xF8\x00", b"\x00\x1F\x00\x00\x00\x03\x03\x02\x01\x04\x02" + b"\x00"*77 + b"\x05\x00", b"\x00\x1F\x00\x00\x00\x03\x03\x00\x01\x04\x01" + b"\x00"*77 + b"\x04\x00"]
}
if args.logo is not None:
    for msg in logo_msg[args.logo]:
        dev.ctrl_transfer(0x21, 0x9, 0x0300, 0x2, msg)
        dev.ctrl_transfer(0xA1, 0x1, 0x0300, 0x2, 0x5A)

# configure keyboard rgb
if args.rgb is None:
    quit()
rgb = reduce(lambda x, y: x + y.to_bytes(1, "big"), args.rgb, b"") * 15
rgb_msg = [
    b"\x00\x1F\x00\x00\x00\x34\x03\x0B\xFF\x00\x00\x0F\x00\x00\x00" + rgb + b"\x00"*30,
    b"\x00\x1F\x00\x00\x00\x34\x03\x0B\xFF\x01\x00\x0F\x00\x00\x00" + rgb + b"\x00"*30,
    b"\x00\x1F\x00\x00\x00\x34\x03\x0B\xFF\x02\x00\x0F\x00\x00\x00" + rgb + b"\x00"*30,
    b"\x00\x1F\x00\x00\x00\x34\x03\x0B\xFF\x03\x00\x0F\x00\x00\x00" + rgb + b"\x00"*30,
    b"\x00\x1F\x00\x00\x00\x34\x03\x0B\xFF\x04\x00\x0F\x00\x00\x00" + rgb + b"\x00"*30,
    b"\x00\x1F\x00\x00\x00\x34\x03\x0B\xFF\x05\x00\x0F\x00\x00\x00" + rgb + b"\x00"*30,
    b"\x00\x1F\x00\x00\x00\x02\x03\x0A\x05\x00\x00\x00\x00\x00\x00" + b"\x00"*75
]
for msg in rgb_msg:
    dev.ctrl_transfer(0x21, 0x9, 0x0300, 0x2, msg)