#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time
import sys

from r305 import genImg, Img2Tz, Search

def setBaud(ser):
    ser.baudrate = 57600

def write(ser):

    
    #first finger scan
    setBaud(ser)    
    data = genImg.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    genImg.parse(s)
    # generate character file of the finger image.
    setBaud(ser)
    data = Img2Tz.getHeader(0x01)
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    Img2Tz.parse(s)

    setBaud(ser)
    data = Search.getHeader(0x01, 0x0000, 0x0064)
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    print Search.parse(s)


ser = serial.Serial(sys.argv[1], sys.argv[2])
write(ser)
