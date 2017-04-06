#!/usr/bin/env python
# -*- coding: utf-8 -*-
header = [0xef,0x01]
address = [0xff,0xff,0xff,0xff]

packet = {

    "COMMAND" : 1,
    "DATA"    : 2,
    "ACK"     : 7,
    "EOP"     : 8
}

instruction = {

    "GenImg"        : 0x01,
    "Img2Tz"        : 0x02,
    "Match"         : 0x03,
    "Search"        : 0x04,
    "RegModel"      : 0x05,
    "Store"         : 0x06,
    "LoadChar"      : 0x07,
    "UpChar"        : 0x08,
    "DownChar"      : 0x09,
    "UpImage"       : 0x0A,
    "DownImage"     : 0x0B,
    "DeletChar"     : 0x0C,
    "Empty"         : 0x0D,
    "SetSysPara"    : 0x0E,
    "ReadSysPara"   : 0x0F,
    "SetPwd"        : 0x12,
    "VfyPwd"        : 0x13,
    "GetRandomCode" : 0x14,
    "SetAdder"      : 0x15,
    "Control"       : 0x17,
    "WriteNotePad"  : 0x18,
    "ReadNotePad"   : 0x19,
    "TemplateNum"   : 0x1d,
}


command_ack = {
    0x00: 'commad execution complete',
    0x01: 'error when receiving data package', 
    0x02: 'no finger on the sensor', 
    0x03: 'fail to enroll the finger',   
    0x06: 'fail to generate character file due to the over-disorderly fingerprint image', 
    0x07: 'fail  to  generate  character  file  due  to  lackness  of character  point  or  over-smallness  of fingerprint image',
    0x08: "finger doesnt match", 
    0x09: 'fail to find the matching finger', 
    0x0A: 'fail to combine the character files', 
    0x0B: 'addressing PageID is beyond the finger library', 
    0x0C: 'error when reading template from library or the template is invalid', 
    0x0D: 'error when uploading template', 
    0x0E: "Module can't receive the following data packages",
    0x0F: 'error when uploading image', 
    0x10: 'fail to delete the template', 
    0x11: 'fail to clear finger library', 
    0x13: 'wrong password!',
    0x15: 'fail to generate the image for the lackness of valid primary image', 
    0x18: 'error when writing flash', 
    0x19: 'No definition error', 
    0x1A: 'invalid register number', 
    0x1B: 'incorrect configuration of register', 
    0x1C: 'wrong notepad page number',
    0x1D: 'fail to operate the communication port', 
}

InsPacketLen = {

    "GenImg"        : [0x00, 0x03],
    "Img2Tz"        : [0x00, 0x04],
    "Match"         : [0x00, 0x03],
    "Search"        : [0x00, 0x08],
    "RegModel"      : [0x00, 0x03],
    "Store"         : [0x00, 0x06],
    "LoadChar"      : [0x00, 0x06],
    "UpChar"        : [0x00, 0x04],
    "DownChar"      : [0x00, 0x04],
    "UpImage"       : [0x00, 0x03],
    "DownImage"     : [0x00, 0x03],
    "DeletChar"     : [0x00, 0x07],
    "Empty"         : [0x00, 0x03],
    "SetSysPara"    : [0x00, 0x05],
    "ReadSysPara"   : [0x00, 0x03],
    "SetPwd"        : [0x00, 0x07],
    "VfyPwd"        : [0x00, 0x07],
    "GetRandomCode" : [0x00, 0x03],
    "SetAdder"      : [0x00, 0x07],
    "Control"       : [0x00, 0x04],
    "WriteNotePad"  : [0x00, 0x36],
    "ReadNotePad"   : [0x00, 0x04],
    "TemplateNum"   : [0x00, 0x03],


}


Checksum = {

    "GenImg"        : [0x00, 0x05],
    "Match"         : [0x00, 0x07],
    "RegModel"      : [0x00, 0x09],
    "UpImage"       : [0x00, 0x0E],
    "DownImage"     : [0x00, 0x0F],
    "Empty"         : [0x00, 0x11],
    "GetRandomCode" : [0x00, 0x18],
    "TemplateNum"   : [0x00, 0x21],
}

def generateHeader():
    return header+address
