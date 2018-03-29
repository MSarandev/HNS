# Created by Maxim Sarandev (1406519)
# January-June 2018
# All Rights Reserved

# Purpose: extract all useful information from a text dump

import datetime, requests, base64
from Tkinter import *

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

    # Encrypt the packet
    def encryptFile(self, file, key):
        """

        Code found on https://gist.github.com/ilogik/6f9431e4588015ecb194
        Modified to a minimum extent
        Based on Vigenere cipher

        """
        file_to_save = open("EE_"+file, 'a')  # define the file

        with open(file) as f:
            lines = f.readlines()  # feed line by line

            for line_x in lines:
                encoded_chars = []  # define the char container
                for i in xrange(len(line_x)):
                    # for each char in the key
                    key_c = key[i % len(key)]
                    # fetch the char in the line
                    encoded_c = chr(ord(line_x[i]) + ord(key_c) % 256)
                    # encrypt the char
                    encoded_chars.append(encoded_c)
                # re-create the string for this line
                encoded_string = "".join(encoded_chars)
                # save to the file
                file_to_save.write(base64.urlsafe_b64encode(encoded_string)+"\r\n")

        # close the files to free resources
        f.close()
        file_to_save.close()

    # Visualisation function
    def visualise(self):
        # define the root container
        root = Tk()

        # define the title for the root container
        root.title("Felis Lynx activity control")

        # assign the root container to be top-most and full screen
        root.attributes("-topmost", True)
        root.attributes("-fullscreen", True)

        # assign focus to the root container
        root.grab_set()

        # create the label with options
        warning_text = Label(root,
                             text="SECURITY ALERT\n\nMonitor mode enabled",
                             relief=FLAT,
                             fg="red",
                             height=root.winfo_screenheight(),
                             width=root.winfo_screenwidth(),
                             font=("Courier", 44),
                             bg="black")

        # close definition
        warning_text.pack()

        # external call to disable the mouse
        #self.lockMouse()

        # run loop
        root.mainloop()

    # Disable the mouse function
    #def lockMouse(self):
    #    hm = pyHook.HookManager()
    #    hm.MouseAll = False
    #    hm.HookMouse()

    # Decrypt Function (DEBUG __ REMOVE IN DEPLOY)
    def decryptFile(self, file, key):
        file_to_save = open("DE_" + file, 'a')

        with open(file) as f:
            lines = f.readlines()

            for line_x in lines:
                # Test decode
                decoded_chars = []
                string = base64.urlsafe_b64decode(line_x)
                for i in xrange(len(string)):
                    key_c = key[i % len(key)]
                    encoded_c = chr((ord(string[i]) - ord(key_c)) % 256)
                    decoded_chars.append(encoded_c)
                decoded_string = "".join(decoded_chars)
                file_to_save.write(decoded_string)

        f.close()
        file_to_save.close()
