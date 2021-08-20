#!/usr/bin/env python3

from PIL import Image, ImageSequence
from easyhid import Enumeration
from time import sleep
from signal import signal, SIGINT, SIGTERM
from sys import exit, argv


def getdevice():
	# Stores an enumeration of all the connected USB HID devices
	en = Enumeration()

	# Return a list of devices based on the search parameters
	# Apex 7
	devices = en.find(vid=0x1038, pid=0x1612, interface=1)
	if not devices:
		# Apex 7 TKL
		devices = en.find(vid=0x1038, pid=0x1618, interface=1)
	if not devices:
		# Apex Pro
		devices = en.find(vid=0x1038, pid=0x1610, interface=1)
	if not devices:
		exit("No devices found, exiting.")

	# Use first device found with vid/pid
	dev = devices[0]
	return dev

def main():
	# Check for arguments
	if(len(argv) != 2):
		exit("Usage: oled.py image.gif\n" +
			 "Static images are supported, too but be careful that they don't burn in.\n" +
			 "You can use 'oled.py none' to just blank the screen.")

	# get our keyboard
	dev = getdevice()

	# define our signal handler to blank the screen on shutdown
	def signal_handler(sig, frame):
		try:
			dev.send_feature_report(bytearray([0x61] + [0x00] * 641))
			dev.close()
			print("\n")
			exit(0)
		except Exception as e:
			exit(str(e))


	# Set up ctrl-c handler
	signal(SIGINT, signal_handler)
	# Set up SIGTERM handler
	signal(SIGTERM, signal_handler)
	dev.open()

	# just blank the screen when we got 'none' as argument
	argument = argv[1]
	if "none" == argument.lower():
		print("blanking the screen")
		signal_handler(SIGTERM, None)
	print("Press Ctrl-C to exit.\n")

	# read the GIF
	try:
		im = Image.open(argument)
	except Exception:
		exit("The GIF " + argument + " can't get opened")

	# resize GIF, process the image frames for the keyboard
	resizedframes = []
	for frame in ImageSequence.Iterator(im):
			# Image size based on Apex 7 and Apex Pro
			frame = frame.resize((128, 40))
			# Convert to monochrome
			frame = frame.convert('1')
			data = frame.tobytes()
			resizedframes.append(bytearray([0x61]) + data + bytearray([0x00]))

	# set up the frame rate
	if 'duration' in frame.info:
		sleeptime = frame.info['duration'] / 1000
	else:
		# we got a single image, we will sleep for one second.
		sleeptime = 1

	# send the frames to the keyboard
	while(1):
		for data in resizedframes:
			dev.send_feature_report(data)
			sleep(sleeptime)
	dev.close()

if __name__ == "__main__":
	main()