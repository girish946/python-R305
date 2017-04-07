import serial
import time
from r305 import *

def getHeader(command, params=None):

    if command in instruction:
        head = header+address
        head.append(packet['COMMAND'])
        pack = head+InsPacketLen[command]
        pack.append(instruction[command])
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
    #print(hex(csum1), hex(csum2))
    return [csum1, csum2]

def getInt(c):
    #print(c)
    if type(c) == int:
        return c
    elif type(c) == str and len(c) == 1:
        return int(ord(c))
    else:
        return None

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

    print("parsing lenght {len}".format(len=len(RecivedDataFrame)))
    print(RecivedDataFrame)
    if header == RecivedDataFrame['header']:
        print("header ok")
        if address == RecivedDataFrame['address']:
            print('address ok')
            if getChecksum(data[:-2]) == RecivedDataFrame['Csum']:
                print("checksum ok")
                print(command_ack[RecivedDataFrame['Ccode']])
                return {'status': RecivedDataFrame['Ccode'],
                        'Csum'  : 'ok',
                        'Data'  : RecivedDataFrame['Data']}
            else:
                print(RecivedDataFrame['Csum'])
                return {'status': RecivedDataFrame['Ccode'],
                        'Csum'  : 'error',
                        'Data'  :  RecivedDataFrame['Data']}

class R305:

    def __init__(self, serialDevice=None, Baudrate=None):

        self.ser = serial.Serial(serialDevice, Baudrate)

    def execute(self, data):
        self.ser.write(bytearray(data))
        time.sleep(1)
        data = self.ser.read(self.ser.inWaiting())
        print([hex(ord(c)) for c in data])
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

    def DeleteAll(self):

        data = getHeader('Empty')
        print([hex(c) for c in data])
        result = self.execute(data)
        return result['status']


    def GenImg(self):

        data = getHeader('GenImg')
        #print([hex(c) for c in data])
        result = self.execute(data)
        #print(result)
        return command_ack[result['status']]

    def Img2Tz(self, bufferId=0x01):

        data = getHeader('Img2Tz', params=[bufferId])
        print([hex(c) for c in data])
        result = self.execute(data)
        return result

    def Match(self):

        data = getHeader('Match')
        print([hex(c) for c in data])
        result = self.execute(data)
        #print(len(result['Data']))
        return result

    def RegModel(self):

        data = getHeader('RegModel')
        print([hex(c) for c in data])
        result = self.execute(data)
        #print(len(result['Data']))
        return result


    def Store(self, bufferId=0x01, templateNum=None):

        if not templateNum:
            templateNum = self.TemplateNum()
        data = getHeader('Store',
                        params=[bufferId, templateNum/100, templateNum%100])
        print([hex(c) for c in data])
        result = self.execute(data)
        return result


    def Search(self, bufferId=0x01, startPage=0x0000, pageNum=0x0064):

        startPage1  = startPage / 100
        startPage2  = startPage % 100

        pageNum1 = pageNum / 100
        pageNum2 = pageNum % 100

        data = getHeader('Search', params=[bufferId, startPage1, startPage2,
                                           pageNum1, pageNum2])
        print([hex(c) for c in data])
        result = self.execute(data)
        return result
