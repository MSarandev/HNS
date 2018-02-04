# Created by Maxim Sarandev (1406519)
# January-June 2018
# All Rights Reserved

# Purpose: extract all useful information from a text dump

import datetime, requests

class Extractor:
    def __init__(self,id):
        self.file_location = ""
        self.string_return = ""
        self.time_stamp = datetime.datetime.now()
        self.id = id  # give the tracker a unique id

    # simply generates a new timestamp
    def newTimeStamp(self):
       self.time_stamp = datetime.datetime.now()

    # Custom method
    # Data extraction below
    def extractData(self, file_path, file_prefix):
        with open(file_path) as f:
            lines = f.readlines()

            # int the counter
            count = 0

            for line_x in lines:
                if(line_x[:3] == "BSS"):
                    # the line contains the MAC address

                    # fetch the mac
                    self.string_return += str(count) + ", "
                    # splice the string, to return the mac only
                    self.string_return += line_x[3:line_x.find("(")]

                    # for ease of use
                    self.string_return += ","

                    # increment the counter
                    count += 1

                # look for the signal strength
                if("signal:" in line_x):
                    # splice the string to return the signal only
                    self.string_return += line_x[line_x.find(":")+1:line_x.find("/n")]

                    # for ease of use
                    self.string_return += ","

                # look for the ESSID
                if("SSID:" in line_x):
                    # splice and push to string
                    self.string_return += line_x[line_x.find(":")+1:line_x.find("/n")]

                    # add the timestamp and end line
                    self.newTimeStamp()
                    self.string_return += ", " + str(self.time_stamp)
                    self.string_return += "\r\n"

            # close the file
            f.close()

            # open the save file, push, close
            f = open(self.id + file_prefix, 'a')
            f.write(self.string_return)
            f.close()

    # Server Health-check
    def checkHealth(self, srv_address):
        # Send a test check
        try:
            ret_string = requests.get("http://" + srv_address,
                                      timeout=2)

            return 200
        except requests.exceptions.ConnectTimeout,\
                requests.exceptions.ReadTimeout:
            return 503  # connection timeout

    # Server Upload file
    def uploadFile(self, srv_address, file):
        files = {'file': open(file, 'rb')}  # define the file

        # push the file via the address
        r = requests.post("http://" + srv_address,
                          files=files, timeout=5)

        r.close()  # close the conn