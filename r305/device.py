import serial
import time
from r305 import *
from __future__ import print_function

def getHeader(command, params=None):
    """
    Generates the command packet for the given instruction of R305.

    :params command: the command for which the packet/header is to be generated.

    :params params: extra parameters if the command need them.
    for example for Img2Tz command you have to specify the buffer Id to store the template.

    Returns command packet for the given instruction, this is a list of bytes.
    """

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
    """
    calculates the checksum of the packet.

    :param data: the datapacket

    Returns the list containing two bytes which are the checksum of the given
    packet.
    """

    frame = data[6:]
    csum = sum(getIntList(frame))
    csum1 = csum / 100
    csum2 = csum % 100
    #print(hex(csum1), hex(csum2))
    return [csum1, csum2]

def getInt(c):
    """
    get the integer value of byte.

    :param c: char/byte

    Returns the integer from the byte
    """

    #print(c)
    if type(c) == int:
        return c
    elif type(c) == str and len(c) == 1:
        return int(ord(c))
    else:
        return None

def getIntList(data):
    """
    Returns the list of ints from the list of chars.
    """

    return [getInt(c) for c in data]

def parse(data):
    """
    Parses the recived data packet.

    Returns the Dict containing:

        status : whether command executed correctly or not.
        Csum   : "ok" if checksum is ok and "error" if there is a checksum error
        Data   : list of bytes if any data is returned by the module.

    """

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
    """
    R305 device object. Contain methods for performaing different
    operations on R305 fingerprint module.
    :param serialDevice: the tty device to which the R305 is connected.
    :param Baudrate: the baudrate over which R305 is operated.
    """

    def __init__(self, serialDevice=None, Baudrate=None):

        self.ser = serial.Serial(serialDevice, Baudrate)

    def execute(self, data):
        """
        Executed the command on the fingerprint module.
        :param data: the data packet.
        writes the data packet to the serial device and parses the result.
        """
        
        self.ser.write(bytearray(data))
        time.sleep(1)
        data = self.ser.read(self.ser.inWaiting())
        #print([hex(ord(c)) for c in data])
        return parse(data)
           

    def TemplateNum(self):
        """
        Retrives the current template number from the fingerprint module.
        """
        
        data = getHeader('TemplateNum')
        #print([hex(c) for c in data])
        result = self.execute(data)
        if result['status'] == 0:
            tnum = getIntList(result['Data'])
            return (256 * tnum[0]) + (tnum[1])
        else:
            return command_ack[result['status']]

    def DeleteAll(self):
        """
        Deletes all of the existing templates from the database.
        """
        
        data = getHeader('Empty')
        #print([hex(c) for c in data])
        result = self.execute(data)
        return result['status']


    def GenImg(self):
        """
        Detects a finger and stores the finger image in the image buffer.
        """
        
        data = getHeader('GenImg')
        #print([hex(c) for c in data])
        result = self.execute(data)
        #print(result)
        return command_ack[result['status']]

    def Img2Tz(self, bufferId=0x01):
        """
        Generates character file from the original finger image in ImageBuffer and
        store the file in CharBuffer1 or CharBuffer2.
        :param bufferId: the CharBuffer where the fingerprint has to be saved.
        """
        
        data = getHeader('Img2Tz', params=[bufferId])
        #print([hex(c) for c in data])
        result = self.execute(data)
        return result

    def Match(self):

        data = getHeader('Match')
        #print([hex(c) for c in data])
        result = self.execute(data)
        #print(len(result['Data']))
        return result

    def RegModel(self):

        data = getHeader('RegModel')
        #print([hex(c) for c in data])
        result = self.execute(data)
        #print(len(result['Data']))
        return result


    def Store(self, bufferId=0x01, templateNum=None):

        if not templateNum:
            templateNum = self.TemplateNum()
        data = getHeader('Store',
                        params=[bufferId, templateNum/100, templateNum%100])
        #print([hex(c) for c in data])
        result = self.execute(data)
        return result


    def Search(self, bufferId=0x01, startPage=0x0000, pageNum=0x0064):

        startPage1  = startPage / 100
        startPage2  = startPage % 100

        pageNum1 = pageNum / 100
        pageNum2 = pageNum % 100

        data = getHeader('Search', params=[bufferId, startPage1, startPage2,
                                           pageNum1, pageNum2])
        #print([hex(c) for c in data])
        result = self.execute(data)
        return result


    def DeletChar(self, pageId=None, n=0):

        pageByte1 = pageId / 100
        pageByte2 = pageId % 100

        nop1 = n / 100
        nop2 = n % 100
        data = getHeader('DeletChar', params=[pageByte1, pageByte2, nop1, nop2])
        result = self.execute(data)
        return result


    def UpChar(self, bufferId=0x01):

        data = getHeader('UpChar', params=[bufferId])
        result = self.execute(data)
        print(result)
        charData = self.ser.read(ser.inWaiting())
        char = [hex(ord(i)) for i in charData]
        print(char)
        return result, charData


    def DownChar(self, bufferId=0x01, pageNumber=0x0000):

        pageByte1 = pageNumber / 100
        pageByte2 = pageNumber % 100
        data = getHeader('DownChar', params[bufferId, pageByte1, pageByte2])
        result = self.execute(data)
        return result


    def StoreFingerPrint(self, callback=print, IgnoreChecksum=True,
                         message="put the finger again ")
                        ):

        if IgnoreChecksum:

            slef.GenImg()
            self.Img2Tz(bufferId=0x01)
            callback(message)
            self.GenImg()
            self.Img2Tz(bufferId=0x02)
            matchResult = self.Match()

            if matchResult['status'] == 0x00:
                searchResult = self.Search(0x01)
                if searchResult['status'] == 0x00:                    
                    self.RegModel()
                    return self.Store()
                elif searchResult['status'] == 0x09:
                    return "finger already present."
                else:
                    return "error while reciving packet"

            elif matchResult['status'] == 0x08:
                return "templates of the two fingers not matching"

            else:
                return "error while reciving packet"
        else:

            slef.GenImg()
            self.Img2Tz(bufferId=0x01)
            callback(message)
            self.GenImg()
            self.Img2Tz(bufferId=0x02)
            self.Match()
            self.Search(0x01)
            self.RegModel()
            return self.Store()

