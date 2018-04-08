# Created by Maxim Sarandev (1406519)
# January-June 2018
# All Rights Reserved

# Purpose: extract all useful information from a text dump

import datetime, base64, os, requests
# DOESN'T WORK OUTSIDE OF LINUX
import pyudev
from Tkinter import *

class Extractor:
    def __init__(self,id):
        self.file_location = ""
        self.string_return = ""
        self.time_stamp = datetime.datetime.now()
        self.id = id  # give the tracker a unique id
        # define the variables
        # allows for easy changes
        self.server_address = "192.168.0.25:8000"
        self.file_name = "test.txt"
        self.file_prefix = "_Capture.txt"
        self.net_adapter = "eth0"
        self.encrypted_prefix = "EE_"
        # REMOVE IN DEPLOY
        self.encrypt_key = "74e6f7298a9c2d168935f58c001bad88"
        # set up the USB monitoring
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='usb')
        self.key_id = "1-1" # specify the USB key ID


    # simply generates a new timestamp
    def newTimeStamp(self):
       self.time_stamp = datetime.datetime.now()

    # Custom methods


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

    # Tracking function
    def tracking(self):
        # call to block the UI
        # ! WARNING !
        # "LOCKS" DEVICE UI, NO INTERACTION POSSIBLE
        # ! WARNING !
        self.visualise()

        # run the script in terminal (list all networks)
        os.system("iw dev " + self.net_adapter +
                  " scan | cat > " + self.file_name)

        # call to extract the data received
        self.extractData(self.file_name, self.file_prefix)

        # encrypt the file
        self.encryptFile(self.id + self.file_prefix,
                         self.encrypt_key)

        # check the connection with the server
        conn_status = self.checkHealth(self.server_address)

        # if a connection can be established with the server...
        if conn_status == 200:
            # attempt transfer
            try:
                # call to the upload function
                self.uploadFile(self.server_address,
                                self.encrypted_prefix +
                                self.id + self.file_prefix)
            except requests.ConnectionError:
                # connection failed, for debug print info
                print "CE-1"

    # Monitor the USB activity
    def monitorUsb(self):
        # start the module
        self.monitor.start()

        # iterate over all USB devices
        for device in iter(self.monitor.poll, None):

            # look for the key
            if device.sys_name == self.key_id:
                # device lost, trigger the tracking
                print "Tracking ON"
                self.tracking()