#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

setup(
    name = 'R305' ,
    version = '1.0.0' ,
    author = 'girish joshi' ,
    author_email = 'girish946@gmail.com' ,
    description = ("""python api for R305 finger print module""") ,
    packages = ['r305'], 
    install_requires = ['pyserial'], 
    keywords = 'python api for R305 finger print module' ,
    scripts = ['Verify.py'], 
    long_description = """python api for R305 finger print module""",
    
  )
