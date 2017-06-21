#!/usr/bin/env python
# -*- coding: utf-8 -*-

from r305 import R305
import sys

device   = sys.argv[1]
baudrate = sys.argv[2] # the default baudrate for this module is 57600

dev = R305(device, baudrate)

def callback(data):
    x = raw_input(data)

result = dev.StoreFingerPrint(IgnoreChecksum=True, callback=callback)
print(result)
