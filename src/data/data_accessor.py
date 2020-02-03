"""This module opens a connection to the remote storage location."""
import os
from base64 import decodebytes
from pysftp import Connection, CnOpts
from paramiko.ecdsakey import ECDSAKey
#from dotenv import find_dotenv, load_dotenv
#above line is only necessary if this is not run in tandem with make_dataset.py

#load_dotenv(find_dotenv())
#above line is only necessary if this is not run in tandem with make_dataset.py

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
