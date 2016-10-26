#!/usr/bin/env python
# -*- coding: utf-8 -*-


from R305 import generateHeader, header, address

identifire = {1:"command packet",
              2: "data packet",
              7:"acknokedge packet",
              8:"end of data packte"}

confirmation_codes = {0:"Found Matching Finger",
                      1:"error while reciving packet",
                      0x09:"No Matching in the Library"}




def parse(s):
    recived_header = s[:2]
    recived_address = s[2:6]
    recived_id = s[6]
    recived_length = s[7:9]
    recived_c_code = s[9]
    recived_Page_id = s[10:11]
    recived_Match_store= s[11:12]
    recived_c_sum = s[12:13]
    if( header == [int(ord(c)) for c in recived_header]):
        if( address == [int(ord(c)) for c in recived_address]):

            print "address and header ok"
            
            #print hex(ord(recived_id))
            #print int(ord(recived_id))
            #print identifire

            print(identifire[int(ord(recived_id)) ])

            #print ([hex(ord(c)) for c in recived_length])

            print (confirmation_codes[int(ord(recived_c_code))])
            print("Page id :"+str(int(ord(recived_Page_id))))
            print("Match Store"+str(int(ord(recived_Match_store))))
            
    return int(ord(recived_Page_id)), int(ord(recived_Match_store))



def getHeader(buf,startpage, pageno):
    data = [0x01, 0x00, 0x08 ,0x04, buf]
    startpage1  = startpage / 100
    startpage2 = startpage % 100
    pageno1 = pageno / 100
    pageno2 = pageno % 100
    csum = sum(data+[startpage1, startpage2, pageno1, pageno2])
    csum1 = csum / 100
    csum2 = csum % 100
    return generateHeader()+ data + [startpage1, startpage2, pageno1, pageno2, csum1, csum2]
