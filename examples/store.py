import serial
import time
from r305 import genImg, Img2Tz, RegModel, TemplateNum, Store, Match
import sys

ser = serial.Serial(sys.argv[1])


def setBaud():
    ser.baudrate = 57600


def write(callback= None):

    
    #first finger scan
    callback("put finger to scan")
    yield
    
    setBaud()    
    data = genImg.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    genImg.parse(s)

    # generate character file of the finger image.
    callback("generating character file "+ "1")
    

    data = Img2Tz.getHeader(0x01)
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    Img2Tz.parse(s)


    #second finger scan.
    callback("again put finger to scan")
    yield
    
   
    data = genImg.getHeader()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    genImg.parse(s)

    #generate character file of the finger image.
    callback("generating character file "+ "1")
    
    data = Img2Tz.getHeader(0x02)
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    Img2Tz.parse(s)

    data = Match.getHeader()
    #print "mathc header is ", [hex(ord(c)) for c in data]
    print "the length of match header is ", len(data)
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print([hex(ord(c)) for c in s])
    match, match_score = Match.parse(s)
    if match == 0:
        #create RegModel
        callback("creating reg model")
    
        data = RegModel.getHeader()
        ser.write(bytearray(data));
        time.sleep(1)
        s = ser.read(ser.inWaiting())
        print([hex(ord(c)) for c in s])
        RegModel.parse(s)
        #getTemplateNumber
        callback("getting template number")
    
        data = TemplateNum.getHeader()
        ser.write(bytearray(data));
        time.sleep(1)
        s = ser.read(ser.inWaiting())
        print([hex(ord(c)) for c in s])
        num = TemplateNum.parse(s)
        callback("template num is "+str(num))
        print "recived template Number is "+ str(num)
    
    
        data = Store.getHeader(0x01,int(num)+1 )
        print([hex(c) for c in data])
        ser.write(bytearray(data));
        time.sleep(1)
        s = ser.read(ser.inWaiting())
        print([hex(ord(c)) for c in s])
        print len(s)
        Store.parse(s)

        #getTemplateNumber
        data = TemplateNum.getHeader()
        ser.write(bytearray(data));
        time.sleep(1)
        s = ser.read(ser.inWaiting())
        print([hex(ord(c)) for c in s])
        num = TemplateNum.parse(s)
        callback("template stored at "+str(num + 1))
        print "recived template Number is "+ str(num)
        return
        
    else:
        print "the two fingers don't match"
        return
    
    
    
def something(msg):
   print msg
if __name__ == '__main__':
    d = write(something)
    while True:
        try:
            d.next()
        except:
            break
