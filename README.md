# python-R305
python api for [R305](http://robokits.co.in/sensors/r305-fingerprint-scanner-module)
Fingerprint module over UART.

![Alt R305 fingerprint module](img/R305.jpg)

    each module contains getHeader() and parse() methods.

    getHeader() generates the frame for the command for the specific instruction.

    the parse() for theat module parses the response of the command and shows the result.

## installation

### using pip

    $ pip install R305

### For Fedora and centos

    $ dnf copr enable girish946/R305
    $ dnf install python-R305

## Documentation

the documentation for Python-R305 package can be found at [rtfd.org](http://python-r305-documentation.readthedocs.io/en/latest/index.html)
