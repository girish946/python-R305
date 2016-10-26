#!/usr/bin/env python
# -*- coding: utf-8 -*-

from R305 import generateHeader, header, address


identifire = {1:"command packet",
              2: "data packet",
              7:"acknokedge packet",
              8:"end of data packte"}

def parse(s):
    recived_header = s[:2]
    recived_address = s[2:6]
    recived_id = s[6]
    recived_length = s[7:9]
    recived_data = s[9:-2]
    recived_c_sum = s[-2:]
    #print([hex(ord(c)) for c in s])
    if( header == [int(ord(c)) for c in recived_header]):
        if( address == [int(ord(c)) for c in recived_address]):

            print([hex(ord(c)) for c in recived_data])
            print "address and header ok"
            
            #print hex(ord(recived_id))
            #print int(ord(recived_id))
            #print identifire

            print(identifire[int(ord(recived_id)) ])

            #print ([hex(ord(c)) for c in recived_length])

            #print (confirmation_codes[int(ord(recived_c_code))])
            return recived_data
            
    return "ok"
   
