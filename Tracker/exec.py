# Created by Maxim Sarandev (1406519)
# January-June 2018
# All Rights Reserved

import os
from data_extractor import Extractor

# Check what OS the system is running (Unix - posix, Win - nt)
if (os.name == "posix"):
    # instantiate an extractor
    ex1 = Extractor("0")
    

    # start the monitor
    ex1.monitorUsb()
elif (os.name == "nt"):
    print "Windows is not supported"