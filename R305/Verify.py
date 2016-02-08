import serial
import time

import genImg, Img2Tz, Search

ser = serial.Serial('/dev/ttyAMA0')


def setBaud():
    ser.baudrate = 57600

def write():

    
    #first finger scan
    setBaud()    
    data = genImg.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    genImg.parse(s)
    # generate character file of the finger image.
    setBaud()
    data = Img2Tz.getHeader(0x01)
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    Img2Tz.parse(s)

    setBaud()
    data = Search.getHeader(0x01, 0x0000, 0x0064)
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    print Search.parse(s)


write()
