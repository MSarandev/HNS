# Created by Maxim Sarandev (1406519)
# January-June 2018
# All Rights Reserved

# Purpose: extract all useful information from a text dump


class Extractor:
    def __init__(self):
        self.file_location = ""
        self.string_return = ""

    # Custom method
    def extractData(self, file_path):
        with open(file_path) as f:
            lines = f.readlines()

            # int the counter
            count = 0

            for line_x in lines:
                if(line_x[:3] == "BSS"):
                    # the line contains the MAC address

                    # fetch the mac
                    self.string_return += str(count)
                    # splice the string, to return the mac only
                    self.string_return += line_x[3:line_x.find("(")]

                    # for ease of use
                    self.string_return += ","

                    # increment the counter
                    count += 1

                # look for the signal strength
                if("signal:" in line_x):
                    # splice the string to return the signal only
                    self.string_return += line_x[line_x.find(":"):line_x.find("/n")]

                    # for ease of use
                    self.string_return += ","

                # look for the ESSID
                if("SSID:" in line_x):
                    # splice and push to string
                    self.string_return += line_x[line_x.find(":"):line_x.find("/n")]

                    # end of line
                    self.string_return += "\r\n"