import pymongo
import json
import requests
import socket
import time
import configparser
from pprint import pprint
from configparser import ConfigParser
from pymongo import MongoClient
#import pdb

config = ConfigParser()

#Read the inifile

try:
    f = open('MongoInfoBeacon.ini', 'rb')
except:
    print("Need a MongoInfoBeacon.ini file.  Try copying the example.ini and filling out")
    quit()

config.read('MongoInfoBeacon.ini')

apiKey = config['apiKey']['apikey']
appVersionId = config['appVersionId']['appversionid']
beaconVersionId = config['default']['beaconversionid']
beaconMessageType = config['default']['beaconmessagetype']
run_interval = int(config['default']['run_interval'])
if config['default']['beaconinstanceid'] == 'hostname':
    beaconInstanceId = socket.gethostname()
else:
    beaconInstanceId =config['default']['beaconinstanceid']
mongoConnectionString = config['mongoConnectionString']['mongoconnectionstring']

def master_optime(members):
    moptime = 0
    for i in range(len(members)):
        member = members[i]
        #pdb.set_trace()
        if member["state"] == 1:
            timestamp, temp_moptime = str(member['optime']['ts']).split('(')
            moptime, term = temp_moptime.split(',')
    return int(moptime)

def send_beacon(message):
    myurl = "https://harbor-stream.herokuapp.com/beacon"
    headers = {
        'Content-Type': 'application/json',
        'apiKey': apiKey,
        'beaconVersionId': beaconVersionId,
        'appVersionId': appVersionId,
        'beaconInstanceId': beaconInstanceId,
        'beaconMessageType': beaconMessageType
    }
    print("Beacon Header: ")
    pprint(headers)
    print("Beacon Body: ")
    pprint(body)
    response = requests.post(myurl, headers = headers, json=body)

def status_list(members):
    body={}
    for i in range(len(members)):
            member = members[i]
            #member_conf = members_conf[i]
            # =this line replaces the dots with dashes for JSON
            replica = member["name"].replace(".","-")
            if member["state"] == 1:
                isPrimary = True
            else:
                isPrimary = False
            timestamp, temp_optime = str(members[i]['optime']['ts']).split('(')
            optime, term = temp_optime.split(',')
            if int(optime) == 0:
                replag = "down"
            else:
                replag = abs(int(optime) - master_optime(members))
            body[replica] = {"isPrimary" : isPrimary, 'repLag' : replag}
    return body

client = MongoClient(mongoConnectionString)
keep_running = True

while keep_running:
    rsstatus = client.admin.command('replSetGetStatus')
    members_list = rsstatus["members"]
    body = status_list(members_list)
    send_beacon(body)
    time.sleep(run_interval)
    keep_running = True
