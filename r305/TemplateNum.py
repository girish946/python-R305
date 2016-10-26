#!/usr/bin/env python
# -*- coding: utf-8 -*-

from struct import unpack
from R305 import generateHeader, header, address

identifire = {1:"command packet",
              2: "data packet",
              7:"acknokedge packet",
              8:"end of data packte"}

confirmation_codes = {0:"read complete.",
                      1:"error while reciving package."}

def parse(s):
    recived_header = s[:2]
    recived_address = s[2:6]
    recived_id = s[6]
    recived_length =s[7:9]
    recived_c_code= s[9]
    recived_template_no = s[10:12]
    if( header == [int(ord(c)) for c in recived_header]):
        if( address == [int(ord(c)) for c in recived_address]):

            print "address and header ok"
            print(identifire[int(ord(recived_id)) ])
            print (confirmation_codes[int(ord(recived_c_code))])
            print("template number is: "+str(256*ord(recived_template_no[0]) + ord(recived_template_no[1])))
            if int(ord(recived_c_code)) == 0x00:
                return 256*ord(recived_template_no[0]) + ord(recived_template_no[1])
            else:
                return "error while reciving data"
                

def getHeader():
    return generateHeader()+[0x01, 0x00,0x03,0x1d,0x00,0x21]
