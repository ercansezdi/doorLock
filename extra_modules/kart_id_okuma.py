#!/usr/bin/env python

import signal
import time
import sys

from pirc522 import RFID

run = True
rdr = RFID()
util = rdr.util()
util.debug = True

def toHex(dec):

	x = (dec %16)
	digits = "0123456789ABCDEF"
	rest = dec /16
	return digits[int(rest)] + digits[int(x)]

def end_read(signal,frame):
    global run
    print("\nCtrl+C captured, ending read.")
    run = False
    rdr.cleanup()
    sys.exit()

signal.signal(signal.SIGINT, end_read)

print("Starting")
while run:
    rdr.wait_for_tag()
    (error, data) = rdr.request()
    (error, uid) = rdr.anticoll()
    if not(error):
        print(uid)        UUID= str(toHex(int(uid[0]))) + " " +str(toHex(uid[1]))+ " " +str(toHex(uid[2])) + " " +str(toHex(uid[3]))
        print('XXX :',UUID)
        time.sleep(0.1)
