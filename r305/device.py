from __future__ import print_function
import serial
import time
from r305 import *


def getHeader(command, params=None):

    """
    Generates the command packet for the given instruction of R305.

    :param command: the command for which the packet/header is to be generated.
    :param params: extra parameters if the command need them.
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
                        'Csum'  : 'ok',
                        'Data'  : RecivedDataFrame['Data']}
            else:
                #print(RecivedDataFrame['Csum'])
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
        Generates character file from the original finger image in
        ImageBuffer and store the file in CharBuffer1 or CharBuffer2.
        
        :param bufferId: the CharBuffer where the fingerprint has to be saved.
        
        """
        
        data = getHeader('Img2Tz', params=[bufferId])
        #print([hex(c) for c in data])
        result = self.execute(data)
        return result

    def Match(self):
    
        """
        Carris out precise matching of templates from CharBuffer1 and CharBuffer2.
        Returns  Matching result.
        """
        
        data = getHeader('Match')
        #print([hex(c) for c in data])
        result = self.execute(data)
        #print(len(result['Data']))
        return result

    def RegModel(self):
    
        """
        Combines information of character files from CharBuffer1 and
        CharBuffer2 and generates a template which is stroed back in
        both CharBuffer1 and CharBuffer2
        """
        
        data = getHeader('RegModel')
        #print([hex(c) for c in data])
        result = self.execute(data)
        #print(len(result['Data']))
        return result


    def Store(self, bufferId=0x01, templateNum=None):
    
        """
        Stores the template of specified buffer (Buffer1/Buffer2) at the 
        designated location of Flash library.
        
        :param bufferId:
        :param templateNum: the template number.
        
        """
        
        if not templateNum:
            templateNum = self.TemplateNum()
        data = getHeader('Store',
                        params=[bufferId, templateNum/100, templateNum%100])
        #print([hex(c) for c in data])
        result = self.execute(data)
        result['template'] = templateNum
        return result


    def Search(self, bufferId=0x01, startPage=0x0000, pageNum=0x0064):
    
        """
        Searches the whole finger library for the template that matches the
        one in CharBuffer1 or CharBuffer2. When found, PageID will be returned.
        
        :param bufferId:
        :param startPage: two bytes address of starting page.
        :param pageNum: two bytes address of last page.
        
        Returns the PageID where the matching finger is found.
        """
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
    
        """
        Deletes a segment (N) of templates of Flash library started from
        the specified location (or PageID);
        
        :param pageId:
        :param n: segment.
        
        """
        pageByte1 = pageId / 100
        pageByte2 = pageId % 100

        nop1 = n / 100
        nop2 = n % 100
        data = getHeader('DeletChar', params=[pageByte1, pageByte2, nop1, nop2])
        result = self.execute(data)
        return result


    def UpChar(self, bufferId=0x01):
    
        """
        Uploads the character file or template of CharBuffer1/CharBuffer2 to upper
        computer.
        
        :param bufferId:
        
        """
        
        data = getHeader('UpChar', params=[bufferId])
        result = self.execute(data)
        print(result)
        charData = self.ser.read(ser.inWaiting())
        char = [hex(ord(i)) for i in charData]
        print(char)
        return result, charData


    def DownChar(self, bufferId=0x01, pageNumber=0x0000):
    
        """
        Downloads character file or template from upper computer to
        the specified buffer of Module.
        
        :param bufferId:
        :param pageNumber:
        """
        
        pageByte1 = pageNumber / 100
        pageByte2 = pageNumber % 100
        data = getHeader('DownChar', params[bufferId, pageByte1, pageByte2])
        result = self.execute(data)
        return result


    def StoreFingerPrint(self, callback=print, IgnoreChecksum=False,
                         message="put the finger again ",
                         templateNum=None
                        ):             
                        
        """
        Performs the complete process for storing a finger into the module.
        to store a finger the process is.
        
        1. scan the finger
        
        2. generate a template
        
        3. scan the finger again
        
        4. generate the second template.
        
        5. match the two templates.
        
        6. if the templates are matching store the fingerprint in the specific location in th module.
                    
        :param callback: callbackfunction to get the message at each step.
        :param IgnoreChecksum: ignores the checksum if True
        :param message: message to be shown while scanning the finger second time.
        :param bufferId: the bufferId for the character file.
        :param templateNum: location where the fingerprint has to be stored. 
        """

        if IgnoreChecksum:

            self.GenImg()
            self.Img2Tz(bufferId=0x01)
            callback(message)
            self.GenImg()
            self.Img2Tz(bufferId=0x02)
            matchResult = self.Match()
            #print(matchResult)
            if matchResult['status'] == 0x00:
                searchResult = self.Search(0x01)
                
                if searchResult['status'] == 0x09:                  
                  
                    self.RegModel()
                    result = self.Store(templateNum=templateNum)
                    
                    if result['status'] == 0x00:
                        return result
                        
                    else :
                        #print("store")
                        return command_ack[result['status']]
                else:
                    if searchResult['status'] == 0x00:
                        return "fingerprint already present"
                    else:
                        return command_ack[searchResult['status']]
            else:
                #print("match")
                return command_ack[matchResult['status']]
        else:

            self.GenImg()
            data = self.Img2Tz(bufferId=0x01)
            if data['Csum'] == 'ok':
            
                callback(message)
                self.GenImg()
                data = self.Img2Tz(bufferId=0x02)
                
                if data['Csum'] == 'ok':
                
                    matchResult = self.Match()
                    if (matchResult['Csum'] == 'ok' and
                        matchResult['status'] == 0x00):
                        searchResult = self.Search(0x01)
                        
                        if (searchResult['Csum'] == 'ok' and
                            searchResult['status'] == 0x09):
                            data = self.RegModel()
                            
                            if data['Csum'] == 'ok':
                               result = self.Store(templateNum=templateNum)
                               if result['Csum'] == 'ok':
                                   return result
                                   
                               else:
                                   return "Checksum Error"
                            else:
                                return "Checksum Error"
                                
                        elif not searchResult['status'] == 0x00:
                            return command_ack[searchResult['status']]
                            
                        elif searchResult['status'] == 0x00:
                            return "fingerprint already present"
                            
                        else:
                            return "Checksum Error"
                            
                    elif not matchResult['status'] == 0x00:
                        return command_ack[matchResult['status']]
                        
                    else:
                        
                        return "Checksum Error"
                else:
                    return "Checksum Error"
            else:
                return "Checksum Error"
            
            
    def SearchFingerPrint(self, IgnoreChecksum=False):
   
       """
       Searches the fingerprint in the module.
       Single method which.
       1. scans the fingerprint
       2. generates the character file
       3. searches this character file in the module
       """
   
       if IgnoreChecksum:
           finger_on_sensor = self.GenImg()
           if finger_on_sensor == 'commad execution complete':
               self.Img2Tz(bufferId=0x01)
               result = self.Search(bufferId=0x01)
               if result['status'] == 0x00:
                   result['pageid']     = int(ord(result['Data'][0]))
                   result['matchstore'] = int(ord(result['Data'][1]))
                   return result
               
               else:
                   return command_ack[result['status']]
           else:
               return finger_on_sensor    
       else:
       
           finger_on_sensor = self.GenImg()
           if finger_on_sensor == 'commad execution complete':
               data = self.Img2Tz(bufferId=0x01)
               if data['Csum'] == 'ok':
           
                   result = self.Search(bufferId=0x01)
                   if result['Csum'] == 'ok':
                       if result['status'] == 0x00:
                           result['pageid']     = int(ord(result['Data'][0]))
                           result['matchstore'] = int(ord(result['Data'][1]))
                           return result
                       else:
                           return command_ack[result['status']]
                   else:
                       return "Checksum Error"
               else:
                   return "Checksum Error"
           else:
               return finger_on_sensor
