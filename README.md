# steelseries-oled
Python utility for displaying GIFs on SteelSeries keyboards

Currently made only for the SteelSeries Apex 7 with 128x40 size OLED
Try to change the VID/PID yourself to see if it works with your keyboard.

# Installation
```
Use pip to install easyhid, pillow and if you want to use the statistics app, psutil.
Windows requires the hidapi.dll file which can be downloaded from the zip file here: https://github.com/libusb/hidapi/releases
```

# Usage
```
python oled.py image.gif
or
python sysstats.py
or
python profile.py [1-5]
  where [1-5] is the profile number
```
# Tools
Included are two extra tools, one that will display system stats on the OLED and one that will switch profiles.
