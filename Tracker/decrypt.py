import base64

def decryptFile(file, key, id):
        file_to_save = open("Decrpyted_"+id+".txt", 'a')

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

# ask for the file name
id1 = raw_input("Enter tracker id: ")
key = raw_input("Enter key: ")

file_name = "EE_"+id1+"_Capture.txt"

decryptFile(file_name, key, id1)
