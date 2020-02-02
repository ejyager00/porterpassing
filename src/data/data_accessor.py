import os
from base64 import decodebytes
import pysftp
from paramiko.ecdsakey import ECDSAKey
from dotenv import find_dotenv, load_dotenv
#above line is only necessary if this is not run in tandem with make_dataset

load_dotenv(find_dotenv())
#above line is only necessary if this is not run in tandem with make_dataset

#-------LOAD ENVIRONMENT VARIABLES FOR CONNECTION--------#
hostname = str(os.environ.get("DATA_ADDRESS"))
username = str(os.environ.get("USERNAME"))
password = str(os.environ.get("PASSWORD"))
remote_path = str(os.environ.get("DIRECTORY_PATH"))
key_type = str(os.environ.get("TYPE"))
key = ECDSAKey(data=decodebytes(os.environ.get("KEY").encode()))

#-------HOST KEY-----#
cnopts = pysftp.CnOpts()
cnopts.hostkeys.add(hostname, key_type, key)

#------OPEN CONNECTION------#
with pysftp.Connection(host=hostname, username=username, password=password, cnopts=cnopts) as sftp:

    # Switch to a remote directory
    print(remote_path)
    sftp.cwd(remote_path)

    # Obtain structure of the remote directory
    directory_structure = sftp.listdir_attr()

    # Print data
    for attr in directory_structure:
        print(attr.filename, attr)
