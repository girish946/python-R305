import serial
import time
from r305 import *

def getHeader(command, params=None):

    if command in instruction:
        head = header+address
        head.append(packet['COMMAND'])
        pack = head+InsPacketLen[command]
        pack.append(instruction['TemplateNum'])
        if params:
            pack.extend(params)
        if command in Checksum:
            pack.extend(Checksum[command])
        else:
            csum = getChecksum(pack)
            pack.extend(csum)
        return pack

def getChecksum(data):
    frame = data[6:]
    csum = sum(getIntList(frame))
    csum1 = csum / 100
    csum2 = csum % 100
    return [csum1, csum2]

def getInt(c):
    return int(ord(c))

def getIntList(data):
    return [getInt(c) for c in data]

def parse(data):

    #print("the length of the recived data is {len}".format(len=len(data)))

    RecivedDataFrame  = {
	    'header'  : getIntList(data[:2]),
	    'address' : getIntList(data[2:6]),
	    'id'      : getInt(data[6]),
	    'length'  : getIntList(data[7:9]),
	    'Ccode'   : getInt(data[9]),
	    'Data'    : data[10:-2],
	    'Csum'    : getIntList(data[-2:]),
    }

    #print("parsing lenght {len}".format(len=len(RecivedDataFrame)))
    #print(RecivedDataFrame)
    if header == RecivedDataFrame['header']:
        #print("header ok")
        if address == RecivedDataFrame['address']:
            #print('address ok')
            if getChecksum(data[:-2]) == RecivedDataFrame['Csum']:
                #print("checksum ok")
                #print(command_ack[RecivedDataFrame['Ccode']])
                return {'status': RecivedDataFrame['Ccode'],
                        'Data'  : RecivedDataFrame['Data']}

class R305:

    def __init__(self, serialDevice=None, Baudrate=None):

        self.ser = serial.Serial(serialDevice, Baudrate)

    def execute(self, data):
        self.ser.write(bytearray(data))
        time.sleep(1)
        data = self.ser.read(self.ser.inWaiting())
        #print([hex(ord(c)) for c in data])
        return parse(data)
           

    def TemplateNum(self):
        data = getHeader('TemplateNum')
        #print([hex(c) for c in data])
        result = self.execute(data)
        if result['status'] == 0:
            tnum = getIntList(result['Data'])
            return (256 * tnum[0]) + (tnum[1])
        else:
            return command_ack[result['status']]
