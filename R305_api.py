from r305.R305 import generateHeader, header, address
from r305 import Img2Tz

import serial
import time
import sys
ser = serial.Serial(sys.argv[1], sys.argv[2])


def setBaud():
    ser.baudrate = 57600


def write():
    setBaud()    
    #data =genImg()
    data = Img2Tz.getHeader(0x01)
    print data
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print type(s), len(s)
    print([hex(ord(c)) for c in s])
    print Img2Tz.parse(s)
    
if __name__ == '__main__':
    write()
