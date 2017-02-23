#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
this script allows you to search a fingerprint in the r305 module.
the algorithm for this is
    1: scan a fingerprint
    2: generate a characterfile from this fingerprint
    3: run a search against this characterfile in r305 module.

in the end you will get the "page id" and "match Store" as the output
if the fingerprint is found in the module.
otherwise you will get the output as "No Matching in the Library"
"""

from r305 import genImg, Img2Tz, Search
import serial
import time
import sys


ser = serial.Serial(sys.argv[1], sys.argv[2])

"""
this is the first scan of the finger. here you have to scan the finger
that you want to search in the database/already stored fingerprints
in the module.
"""
command = genImg.getHeader()  #get the dataframe for the command
ser.write(bytearray(command)) #the data must be buyte a array
time.sleep(1)                 #wait for the device to process command
op = ser.read(ser.inWaiting())#read the response of the command 
genImg.parse(op)              #parse the response of the command

"""
here you have to generate the character file in order to search for
the fingerprint in the database/already stored fingerprints
in the module.
"""
# generate character file of the finger image.
command = Img2Tz.getHeader(0x01) #get the dataframe for the command
ser.write(bytearray(command));   #the data must be buyte a array
time.sleep(1)                    #wait for the device to process command
op = ser.read(ser.inWaiting())   #read the response of the command 
Img2Tz.parse(op)                 #parse the response of the command

"""
this is the actual search process.
in this process you have to give the buffer in which you have to search
along with the start and stop of the page.
"""
#get the dataframe for the command
command = Search.getHeader(0x01, 0x0000, 0x0064)
ser.write(bytearray(command));        #the data must be buyte a array
time.sleep(1)                      #wait for the device to process command
op = ser.read(ser.inWaiting())      #read the response of the command 
print Search.parse(op)              #parse the response of the command



