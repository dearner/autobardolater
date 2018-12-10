#!/usr/bin/python

from Adafruit_Thermal import *
import random
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

button = True
button_pin = 12

if button:
    GPIO.setup(button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

printer = Adafruit_Thermal("/dev/serial0", 19200, timeout=5)
printer.writeBytes(0x1B, 0x21, 0x1)

def print_sonnet(num = 0):
    lines = []
    sonnetnum = random.randrange(1, 155)
    if num: sonnetnum = num
    #printer.feed(3)
    with open ("/home/pi/autobardolater/sonnets/" + str(sonnetnum) + ".txt") as f:
        lines = f.readlines()
    # Some sonnets have a trailing blank line.
    # Get rid of newlines, etc, println() adds them anyway
    lines = [k.strip() for k in lines]
    if lines[0] == "":
       lines = lines[1:len(lines)]
    if lines[-1] == "":
        lines = lines[0:-1]
    print lines
    # Add an empty line between the sonnet and the couplet
    rest = lines[14:16]
    print "REST\n"
    print rest
    print "REST\n"
    lines = lines[0:14] + [""] + rest
    print lines
    # exit()
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
            maxlength = 40

        # split long lines into two, and get the right number of tabs
        if len(k) > maxlength:
            if k[0] == "\t":
                str1 = "\t"
                str2 = "\t\t"
            else:
                str1 = ""
                str2 = "\t"

            k = k.strip().split()

            for j in k:
                if len(str1) < 30:
                    str1 += (j) + " "
                else:
                    str2 += (j) + " "
            printer.println(str1)
            printer.println(str2)
        else:
            printer.println(k)

    printer.feed(6)

if len(sys.argv) > 1:
    try:
        print_sonnet(num = int(sys.argv[1]))
    except Exception as e:
        print "argument must be number"
        exit()
    exit()
if not button:
    print_sonnet()
    exit()
else:
    while(1):
        if not GPIO.input(button_pin):
            print_sonnet()

printer.sleep()      # Tell printer to sleep
printer.wake()       # Call wake() before printing again, even if reset
printer.setDefault() # Restore printer to defaults
