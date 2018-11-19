
import pymongo
import json
import requests
import socket
import time
import configparser


from pymongo import MongoClient
from configparser import ConfigParser

config: ConfigParser = configparser.ConfigParser()

#Read the inifile

try:
    f = open('mongo-beacon.ini', 'rb')
except:
    print("Need a mongo-beacon.ini file.  Try copying the example.ini and filling out")
    quit()

config.read('mongo-beacon.ini')

apiKey = config['apiKey']['apikey']
beaconVersionId = config['beaconVersionId']['beaconversionid']
appVersionId = config['appVersionId']['appversionid']
beaconMessageType = config['default']['beaconmessagetype']
run_interval = int(config['default']['run_interval'])
if config['default']['beaconinstanceid'] == 'hostname':
    beaconInstanceId = socket.gethostname()
else:
    beaconInstanceId =config['default']['beaconinstanceid']
mongoConnectionString = config['mongoConnectionString']['mongoconnectionstring']


client = MongoClient(mongoConnectionString)

while True:
    rsstatus = client.admin.command('replSetGetStatus')

    members = rsstatus["members"]
    print(members)

    def list_members():
            body={}
            for i in range(len(members)):
                    member = members[i]
                    # =these line replaces the dots with dashes for JSON
                    replica = member["name"].replace(".","-")
                    if member["stateStr"] == "PRIMARY":
                        isPrimary = 1
                    else:
                        isPrimary = 0
                    body[replica] = {"isPrimary" : isPrimary}
            return body



    body = list_members()

    myurl = "https://harbor-stream.herokuapp.com/beacon"
    headers = {
        'Content-Type': 'application/json',
        'apiKey': apiKey,
        'beaconVersionId': beaconVersionId,
        'appVersionId': appVersionId,
        'beaconInstanceId': beaconInstanceId,
        'beaconMessageType': beaconMessageType
    }
    print(headers)
    print(body)
    response = requests.post(myurl, headers = headers, json=body)
    time.sleep(run_interval)
