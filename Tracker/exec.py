# Created by Maxim Sarandev (1406519)
# January-June 2018
# All Rights Reserved

import os
from data_extractor import Extractor

# Check what OS the system is running (Unix - posix, Win - nt)
if (os.name == "posix"):
    # launch the command and save to test.txt
    res_string = os.system("iw dev wlan0 scan | cat > test.txt")

    # deploy
    ex1 = Extractor()

    # extract the data
    ex1.extractData("test.txt")

elif (os.name == "nt"):
    print "Windows is not supported"