# python-R305
python api for [R305](http://robokits.co.in/sensors/r305-fingerprint-scanner-module)
Fingerprint module over UART.

![Alt R305 fingerprint module](img/R305.jpg)


## installation

### using pip

    $ pip install R305

### For Fedora and centos

    $ dnf copr enable girish946/R305
    $ dnf install python-R305
    
    
## Usage

To store the fingerprint in to the module

```python
from r305 import R305
import sys

device   = sys.argv[1]
baudrate = sys.argv[2] # the default baudrate for this module is 57600

dev = R305(device, baudrate)

def callback(data):
    x = raw_input(data)

result = dev.StoreFingerPrint(IgnoreChecksum=True, callback=callback)
print(result)
```

To search fingerprint in the module

```python
from r305 import R305
import sys

device   = sys.argv[1]
baudrate = sys.argv[2] # the default baudrate for this module is 57600

dev = R305(device, baudrate)

result = dev.SearchFingerPrint()
print(result)
```

## Documentation

the documentation for Python-R305 package can be found at [rtfd.org](http://python-r305-doc.readthedocs.io/en/latest/index.html)
