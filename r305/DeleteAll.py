#!/usr/bin/env python
# -*- coding: utf-8 -*-

from R305 import generateHeader, header, address


identifire = {1:"command packet",
              2: "data packet",
              7:"acknokedge packet",
              8:"end of data packte"}

confirmation_codes = {0:"Empty success",
                      1:"error while reciving packet",
                      0x11:"fail to clear finger library."}




def parse(s):
    recived_header = s[:2]
    recived_address = s[2:6]
    recived_id = s[6]
    recived_length = s[7:9]
    recived_c_code = s[9]
    recived_c_sum = s[10:11]
    if( header == [int(ord(c)) for c in recived_header]):
        if( address == [int(ord(c)) for c in recived_address]):

            print "address and header ok"
            
            #print hex(ord(recived_id))
            #print int(ord(recived_id))
            #print identifire

            print(identifire[int(ord(recived_id)) ])

            #print ([hex(ord(c)) for c in recived_length])

            print (confirmation_codes[int(ord(recived_c_code))])
            return confirmation_codes[int(ord(recived_c_code))]
            
    return "error"



def getHeader():
        return generateHeader()+[0x01, 0x00, 0x03, 0x0d, 0x00, 0x11]
