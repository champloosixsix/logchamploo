import paramiko
from django.shortcuts import render
from dateutil import parser
from .models import Log
from datetime import timedelta
from django.db.models.functions import Now
from environs import Env

env = Env()
env.read_env()

def index(request):
    # connect and login to sftp server
    HOST_NAME,PORT = env.str("FTP_HOST_NAME"),env.int("FTP_HOST_PORT")
    USER_NAME,PASSWORD = env.str("FTP_USER_NAME"),env.str("FTP_PASSWORD")
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=HOST_NAME, port=PORT, username=USER_NAME, password=PASSWORD)
    
    # open sftp folder and create a list of names in dir/keep only the last 20
    sftp_client = client.open_sftp()
    sftp_client.chdir(env.str("FTP_DIR"))
    logArray = [x.filename for x in sorted(sftp_client.listdir_attr(), key = lambda f: f.st_mtime)]  
    shortArray = logArray[-20:]
    newLog = [*set(shortArray)]

    # go through each file and read the lines extracting the data
    for x in newLog:
        file = sftp_client.open(x, 'r')
        content = file.readlines()
        dateLine = content[1]
        lineSplit = dateLine.split('_')
        dateSt = lineSplit[0]
        dateStr = str(dateSt)
        res = parser.parse(dateStr, fuzzy=True)
        catchLine = 'steamid='
        catchLine1 = 'Player'
        catchLine2 = 'Survivor'
        for line in content:
            if catchLine in line and catchLine1 not in line and catchLine2 not in line:
                timeSplit = line.split(' ',1)
                tVal = timeSplit[0]
                pNameb = line.split('"')[1::2]
                pName = pNameb[0]
                steamIdb = line[line.find("(")+1:line.find(")")]
                steamIdc = steamIdb.split("=")
                steamId = steamIdc[1]
                actionB = line.split(")",1)
                action = actionB[1]

                #add the extracted data to the database
                if Log.objects.filter(log_date=res,name=pName,steamid=steamId,action=action,time=tVal).exists():
                    pass
                else:
                    try:
                        Log(log_date=res,name=pName,steamid=steamId,action=action,time=tVal).save()
                    except:
                        pass
    # delete any data thats over 5 days old and re order data
    Log.objects.filter(log_date__lt=Now()-timedelta(days=5)).delete()            
    context = {}
    context["dataset"] = Log.objects.all().order_by("-log_date", "-time")

    return render(request, 'index.html', context)
