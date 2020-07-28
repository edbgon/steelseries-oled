#!/usr/bin/env python3

from PIL import Image, ImageSequence
from easyhid import Enumeration
from time import sleep
import signal
import sys

def signal_handler(sig, frame):
    try:
    	# Blank screen on shutdown
        dev.send_feature_report(bytearray([0x61] + [0x00] * 641))
        dev.close()
        print("\n")
        sys.exit(0)
    except:
        sys.exit(0)

# Check for arguments
if(len(sys.argv) < 2):
	print("Usage: oled.py image.gif\n")
	sys.exit(0)        

# Set up ctrl-c handler
signal.signal(signal.SIGINT, signal_handler)

# Stores an enumeration of all the connected USB HID devices
en = Enumeration()
# Return a list of devices based on the search parameters / Hardcoded to Apex 7
devices = en.find(vid=0x1038, pid=0x1612, interface=1)
if not devices:
    devices = en.find(vid=0x1038, pid=0x1618, interface=1)
if not devices:
    print("No devices found, exiting.")
    sys.exit(0)

# Use first device found with vid/pid
dev = devices[0]

print("Press Ctrl-C to exit.\n")
dev.open()

im = Image.open(sys.argv[1])

while(1):
	for frame in ImageSequence.Iterator(im):
	    
	    # Image size based on Apex 7
	    frame = frame.resize((128, 40))
	    
	    # Convert to monochrome
	    frame = frame.convert('1')
	    data = frame.tobytes()
	    
	    # Set up feature report package
	    data = bytearray([0x61]) + data + bytearray([0x00])

	    dev.send_feature_report(data)
	    sleep(frame.info['duration'] / 1000)

dev.close()
