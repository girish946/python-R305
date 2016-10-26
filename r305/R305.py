#!/usr/bin/env python
# -*- coding: utf-8 -*-
header = [0xef,0x01]
address = [0xff,0xff,0xff,0xff]


def generateHeader():
    return header+address
