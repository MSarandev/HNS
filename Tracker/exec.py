# Created by Maxim Sarandev (1406519)
# January-June 2018
# All Rights Reserved

import os, requests
from data_extractor import Extractor

# Check what OS the system is running (Unix - posix, Win - nt)
if (os.name == "posix"):
    server_address = "192.168.0.25:8000"
    file_name = "test.txt"
    file_prefix = "_Capture.txt"
    net_adapter = "wlan0"

    # launch the command and save to test.txt
    res_string = os.system("iw dev "+ net_adapter +" scan | cat > "+file_name)

    # deploy
    ex1 = Extractor("0")

    # extract the data
    ex1.extractData(file_name, file_prefix)

    conn_status = ex1.checkHealth(server_address)

    # if a connection can be established with the server...
    if(conn_status == 200):
        # attempt transfer
        try:
            ex1.uploadFile(server_address, ex1.id+file_prefix)

            print "Upload OK"
        except ex1 as requests.ConnectionError:
            print "Connection error" + ex1

elif (os.name == "nt"):
    print "Windows is not supported"