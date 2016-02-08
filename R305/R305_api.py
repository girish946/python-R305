import serial
import time
#from R305 import generateHeader, header, address
from R305 import genImg, Img2Tz, RegModel, TemplateNum, DeleteAll, Store

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


    #second finger scan.
    setBaud()    
    data = genImg.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    genImg.parse(s)
    #generate character file of the finger image.
    setBaud()
    data = Img2Tz.getHeader(0x02)
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    Img2Tz.parse(s)


    #create RegModel
    setBaud()    
    data = RegModel.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    RegModel.parse(s)
    #getTemplateNumber
    setBaud()    
    data = TemplateNum.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    num = TemplateNum.parse(s)
    print "recived template Number is "+ str(num)

    """
    setBaud()    
    data = DeleteAll.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    print(DeleteAll.parse(s))"""

    
    setBaud()    
    data = Store.getHeader(0x01,int(num)+1 )
    print([hex(c) for c in data])
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    print len(s)
    Store.parse(s)

     #getTemplateNumber
    setBaud()    
    data = TemplateNum.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    num = TemplateNum.parse(s)
    print "recived template Number is "+ str(num)
    

    
    
    
if __name__ == '__main__':
    write()
