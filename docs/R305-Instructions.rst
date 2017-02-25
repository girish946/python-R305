R305-Instructions
=================

Fingerprint Processing Instructions
-----------------------------------

GenImg
~~~~~~

To collect Finger Image:

    this instruction is used for detecting the finger and store the detected finger image in ImageBuffer while returning successfull confirmation code; If there is no finger, returned conirmation code would be "can't detect finger".

UpImage
~~~~~~~

Upload Image:

    this instruction is used to upload the image in Img_Buffer to upper computer

DownImage
~~~~~~~~~

Download Image:

    to download image from upper computer to Img_Buffer.


Img2Tz
~~~~~~

To generate character file from  image:

    to generate char acter file from the original finger image
     in ImageBuffer and store the file in CharBuffer1 or CharBuffer2.

RegModel
~~~~~~~~

To generate template:

    to combine information of character files from CharBuffer1 and CharBuffer2 and generate a template which is stored back in both CharBuffer1 and CharBuffer2.


UpChar
~~~~~~

To upload character or template:

    to upload the character file or template of CharBuffer1/CharBuffer2 to upper computer.


Store
~~~~~

To store template:

    to store the template of specified buffer (Buffer1/Buffer2) at the designated location of Flash library.

LoadChar
~~~~~~~~

To read template from Flash library:

    to load template at the specified location (PageID) of Flash library to template buffer CharBuffer1/CharBuffer2.


Empty
~~~~~

To empty finger library:

    to delete all the template in the Flash library.

Match
~~~~~

To carry out precise matching of two finger templates:

    to carry out precise matching of templates from CharBuffer1 and CharBuffer2 providing matching results.

Search
~~~~~~

To search finger library:

    to search the wholw finger library for the template that matches the one in the CharBuffer1 or CharBuffer2. When found PageId will be returned.


