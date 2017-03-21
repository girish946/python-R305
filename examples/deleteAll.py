#!/usr/bin/env python
# -*- coding: utf-8 -*-

from r305 import DeleteAll
import sys
import serial
import time

device = sys.argv[1] #this is the serial device (ie R305)
baudrate = sys.argv[2] #this is the baudrate for the serial communication

#generally serial device can be found at /dev/ttyUSBx
#generally the baudrate for r305 is 57600
#although depending upon the driver and configuration these things may vary.

ser = serial.Serial(device, baudrate) #init serial

command = DeleteAll.getHeader()     #get the dataframe for the command
ser.write(bytearray(command));         #the data must be buyte a array
time.sleep(1)                       #wait for the device to process command
response = ser.read(ser.inWaiting())#read all the data that is comming from r305
print(DeleteAll.parse(response))    #parse the output of the command.
