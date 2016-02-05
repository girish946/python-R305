
import serial
import time
ser = serial.Serial('/dev/ttyAMA0')

""" the default header for R305 fingerprint module is 0xEF01
and the default address is 0xFFFFFFFF"""

header = [0xef,0x01]
address = [0xff,0xff,0xff,0xff]


"""
    these identifires are for genImg command,
"""
identifire = {1:"command packet",
              2: "data packet",
              7:"acknokedge packet",
              8:"end of data packte"}

"""
    these confirmation codes are for genImg command.
"""
confirmation_codes = {0:"finger collection success",
                      1:"error when reciving package",
                      2:"can't detect finger",
                      3:"fail to collect finger"}




def setBaud():
    ser.baudrate = 57600



def generateHeader():
    """
        generates the default header byte sequence for the data frame.
    """
    return header+address



def parse(s):
    """
       currently written for parsing the response frame of genImg command only.
       Will be implemented for each and every command.
    """
    recived_header = s[:2]
    recived_address = s[2:6]
    recived_id = s[6]
    recived_length =s[7:9]
    recived_c_code= s[9]

    if( header == [int(ord(c)) for c in recived_header]):
        if( address == [int(ord(c)) for c in recived_address]):

            print "address and header ok"
            
            #print hex(ord(recived_id))
            #print int(ord(recived_id))
            #print identifire

            print(identifire[int(ord(recived_id)) ])

            #print ([hex(ord(c)) for c in recived_length])

            print (confirmation_codes[int(ord(recived_c_code))])
            
    return ""


def genImg():
    return generateHeader()+[0x01,0x00,0x03,0x01,0x00,0x05]

def templatenum():
    return generateHeader()+[0x01, 0x00,0x03,0x1d,0x00,0x21]


def write():
    setBaud()    
    #data =genImg()
    data = templatenum()
    ser.write(bytearray(data));
    time.sleep(1)
    s = ser.read(ser.inWaiting())
    print type(s)
    print([hex(ord(c)) for c in s])
    print parse(s)
    
if __name__ == '__main__':
    write()
