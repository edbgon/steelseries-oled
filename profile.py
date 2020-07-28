#!/usr/bin/env python3

from easyhid import Enumeration
import sys

# Check for arguments
if(len(sys.argv) < 2):
	print("Usage: profile.py profile_number\n")
	sys.exit(0)        

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

dev.open()

data = bytearray([0x89]) + int(sys.argv[1]).to_bytes(16, sys.byteorder) + bytearray([0x00] * 62)
dev.send_feature_report(data)

dev.close()
