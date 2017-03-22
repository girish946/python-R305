#!/usr/bin/env python
# -*- coding: utf-8 -*-

from R305 import generateHeader, header, address
import struct

# Match intruction is used in R305 fingerprint module to carry out
# precise matching of two templates from CharBuffer1 and CharBuffer2


identifire = {1:"command packet",
              2: "data packet",
              7:"acknokedge packet",
              8:"end of data packte"}

confirmation_codes = {0:"Templates of the two buffers are matching!",
                      1:"error while reciving packet",
                      0x08:"templates of the two buffers aren’t matching",
                     }
                     
def parse(s):
    print len(s)
    recived_header = s[:2]
    recived_address = s[2:6]
    recived_id = s[6]
    recived_length = s[7:9]
    recived_conf_code = s[9]
    recived_matching_score = s[10:12]
    recived_checksum = s[12:14]
    print confirmation_codes[int(ord(recived_conf_code))]
    print "accuracy is ", 256*ord(recived_matching_score[0]) +256*ord(recived_matching_score[1])
    return int(ord(recived_conf_code)), recived_matching_score
    
                     

def getHeader():
    data = [0x01, 0x00, 0x03, 0x03, 0x00, 0x07 ]
    #print "generating header ", [hex(c) for c in generateHeader()+ data], len([hex(c) for c in generateHeader()+ data])
    return generateHeader()+ data
