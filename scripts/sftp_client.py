import paramiko, django_extensions
import os
import time, glob, shutil, re
from datetime import datetime
from dateutil import parser


HOST_NAME,PORT = "66.235.173.138",8822
USER_NAME,PASSWORD = "champloosixsix", "Fellybonk1!"

def run():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=HOST_NAME, port=PORT, username=USER_NAME, password=PASSWORD)

    sftp_client = client.open_sftp()
    sftp_client.chdir('66.235.173.138_2302/SC/VPPAdminTools/Logging')
    logArray = sftp_client.listdir()

    for x in logArray:
        if os.path.exists('C:/VSCode/logChamploo/scripts/vppLogs/'+x):
            continue
        else:
            sftp_client.get(x, 'C:/VSCode/logChamploo/scripts/vppLogs/'+x)
    
    newLog = [*set(logArray)]
    for x in newLog:
        file = open('C:/VSCode/logChamploo/scripts/vppLogs/'+x)
        content = file.readlines()
        dateLine = content[1]
        lineSplit = dateLine.split('_')
        dateSt = lineSplit[0]
        dateStr = str(dateSt)
        res = parser.parse(dateStr, fuzzy=True)
        resSlim, dump = res.partition(' ')
        print(resSlim)
        
