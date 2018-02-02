# Created by Maxim Sarandev (1406519)
# January-June 2018
# All Rights Reserved

# This file needs to be as small as possible, no OOP will be implemented
import os

# Check what OS the system is running (Unix - posix, Win - nt)
if (os.name == "posix"):
    res_string = ""

    res_string = os.system("airport -s")

    if(res_string == ""):
        # operation failed, try Linux style command
        res_string = os.system("iw dev wlan0 scan | grep SSID")

    
elif (os.name == "nt"):
    print "Windows yay"