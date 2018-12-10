#!/usr/bin/python

from Adafruit_Thermal import *
import random

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer.writeBytes(0x1B, 0x21, 0x1)
sonnetnum = random.randrange(1, 155)

#printer.feed(3)
with open ("/home/pi/autobardolater/sonnets/" + str(sonnetnum) + ".txt") as f:
    lines = f.readlines()
# Get rid of newlines, etc, println() adds them anyway
lines = [k.strip() for k in lines]

# Add an empty line between the sonnet and the couplet
rest = lines[15:17]
lines = lines[0:15] + [""] + rest
print lines
# and indent the couplet
lines[-1] = "\t" + lines[-1]
lines[-2] = "\t" + lines[-2]

for k in lines:
    # empty line: print a newline
    if not len(k): 
        printer.println()
        continue
    # Set length according to whether or not first char is a tab
    maxlength = 42
    if k[0] == "\t":
        maxlength = 39

    # split long lines into two, and get the right number of tabs
    if len(k) > maxlength:
        if k[0] == "\t":
            str1 = "\t"
            str2 = "\t\t"
        else:
            str1 = ""
            str2 = "\t"
        k = k[0:-1].split()

        for j in k:
            if len(str1) < 30:
                str1 += (j) + " "
            else:
                str2 += (j) + " "
        printer.println(str1)
        printer.println(str2)
    else:
        printer.println(k)

printer.feed(3)

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
