"""This module opens a connection to the remote storage location."""
import os
from base64 import decodebytes
from pysftp import Connection, CnOpts
from paramiko.ecdsakey import ECDSAKey
#from dotenv import find_dotenv, load_dotenv
#above line is only necessary if this is not run in tandem with make_dataset.py

#load_dotenv(find_dotenv())
#above line is only necessary if this is not run in tandem with make_dataset.py

def open_sftp_connection():
    hostname = str(os.environ.get("DATA_ADDRESS"))
    username = str(os.environ.get("USERNAME"))
    password = str(os.environ.get("PASSWORD"))
    key_type = str(os.environ.get("TYPE"))
    key = ECDSAKey(data=decodebytes(os.environ.get("KEY").encode()))
    cnopts = CnOpts()
    cnopts.hostkeys.add(hostname, key_type, key)
    return Connection(host=hostname, username=username,
                      password=password, cnopts=cnopts)

if __name__ == '__main__':
    #-------LOAD ENVIRONMENT VARIABLES FOR CONNECTION--------#
    HOSTNAME = str(os.environ.get("DATA_ADDRESS"))
    USERNAME = str(os.environ.get("USERNAME"))
    PASSWORD = str(os.environ.get("PASSWORD"))
    REMOTE_PATH = str(os.environ.get("DIRECTORY_PATH"))
    KEY_TYPE = str(os.environ.get("TYPE"))
    KEY = ECDSAKey(data=decodebytes(os.environ.get("KEY").encode()))
    #-------HOST KEY-----#
    CNOPTS = CnOpts()
    CNOPTS.hostkeys.add(HOSTNAME, KEY_TYPE, KEY)

    #------OPEN CONNECTION------#
    with Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=CNOPTS) as sftp:

        # Switch to a remote directory
        sftp.cwd(REMOTE_PATH)

        # Obtain structure of the remote directory
        directory_structure = sftp.listdir_attr()

        # Print data
        for attr in directory_structure:
            print(attr.filename, attr)
