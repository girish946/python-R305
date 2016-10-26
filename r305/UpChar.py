#!/usr/bin/env python
# -*- coding: utf-8 -*-

from R305 import generateHeader, header, address
import DataPacket

identifire = {1:"command packet",
              2: "data packet",
              7:"acknokedge packet",
              8:"end of data packte"}

confirmation_codes = {0:"ready to transfer the following data packet.",
                      1:"error while reciving packet",
                      0x0d:"error when uploading datapacket."}




def parse(s):
    recived_header = s[:2]
    recived_address = s[2:6]
    recived_id = s[6]
    recived_length = s[7:9]
    recived_c_code = s[9]
    recived_c_sum = s[10:11]
    recived_data_packet = s[12:]
    if( header == [int(ord(c)) for c in recived_header]):
        if( address == [int(ord(c)) for c in recived_address]):

            print "address and header ok"
            
            #print hex(ord(recived_id))
            #print int(ord(recived_id))
            #print identifire

            print(identifire[int(ord(recived_id)) ])

            #print ([hex(ord(c)) for c in recived_length])

            print (confirmation_codes[int(ord(recived_c_code))])
            DataPacket.parse(recived_data_packet)
            
    return "ok"



def getHeader():
    return generateHeader()+[0x01, 0x00, 0x04 ,0x08, 0x01, 0x00, 0x0e]
