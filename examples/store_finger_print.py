#!/usr/bin/env python
# -*- coding: utf-8 -*-

from r305 import R305
import sys

device   = sys.argv[1]
baudrate = sys.argv[2] # the default baudrate for this module is 57600

dev = R305(device, baudrate)

result = dev.SearchFingerPrint()
print(result)
