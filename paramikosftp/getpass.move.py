#!/usr/bin/python3
## Try a real world test with getpass

## import Paramiko so we can talk SSH
import paramiko # allows Python to ssh
import os # low level operating system commands
import getpass # we need this to accept passwords
import os.path 

    
def transfer_to_dir(t):
    sftp = paramiko.SFTPClient.from_transport(t)
    
    ## copy our firstpasswd.py script to bender
    opath=   input("enter full path")
    isabs = os.path.isabs(opath) 
    while not isabs:
        opath = input ("try again")
        isabs = os.path.isabs(opath) 
    aopath= opath+"oiledpayload.txt"
    sftp.put("payload.txt", "oiledpayload.txt") # move file to target location home directory
    



def main():
    ## where to connect to
    t = paramiko.Transport("10.10.2.3", 22) ## IP and port of bender
    
    ## how to connect (see other labs on using id_rsa private / public keypairs)
    t.connect(username="bender", password=getpass.getpass()) # notice the password references getpass
    
    ## Make an SFTP connection object
    sftp = paramiko.SFTPClient.from_transport(t)
    
    ## copy our firstpasswd.py script to bender
    sftp.put("payload.txt", "oiledpayload.txt") # move file to target location home directory
    
    transfer_to_dir(t)
    ## close the connection
    sftp.close() # close the connection
if __name__ == "__main__":
    main()

