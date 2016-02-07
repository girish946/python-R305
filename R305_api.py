import serial
import time
from R305 import generateHeader, header, address

from Img2Tz import parse, Img2Tz

ser = serial.Serial('/dev/ttyAMA0')


def setBaud():
    ser.baudrate = 57600


def write():
    setBaud()    
    #data =genImg()
    data = Img2Tz()
    print data
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print type(s), len(s)
    print([hex(ord(c)) for c in s])
    print parse(s)
    
if __name__ == '__main__':
    write()
