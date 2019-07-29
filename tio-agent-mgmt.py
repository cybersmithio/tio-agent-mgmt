#!/usr/bin/python

import argparse
import re
from tenable.io import TenableIO
import os

#Attempts to make a connection to Tenable.io
def ConnectIO(DEBUG,accesskey,secretkey,host,port):
    if DEBUG:
        print("Connecting to Tenable.io using access key",accesskey)
    #Create the connection to Tenable.io
    try:
        tio=TenableIO(accesskey, secretkey)
    except:
        print("Error connecting to Tenable.io")
        return(False)

    return(tio)


def listAgents(DEBUG,conn,agentgroup,nogroupflag):



    if agentgroup==None and nogroupflag == False:
        resp=conn.agents.list()

    elif agentgroup != None:
        for i in getAgentGroups(DEBUG, conn):
            if str(i['name']) == agentgroup:
                #resp=conn.agents.list(("groups","eq",str(i['id']) ))
                rawresp = conn.get('scanners/'+getFirstScannerID(DEBUG,conn)+'/agents?f=groups:eq:'+str(i['id']))
                resp=rawresp.json()['agents']
    else:
        rawresp = conn.get('scanners/' + getFirstScannerID(DEBUG, conn) + '/agents?f=groups:eq:-1')
        resp = rawresp.json()['agents']


    print("\nAgent Name (Agent ID)")
    print("---------------------------------")
    for i in resp:
        print(str(i['name']) + " (" + str(i['id']) + ")")


def getFirstScannerID(DEBUG,conn):
    resp=conn.scanners.list()
    return(str(resp[0]['id']))

def getAgentGroups(DEBUG,conn):
    resp=conn.get('scanners/'+getFirstScannerID(DEBUG,conn)+'/agent-groups')

    return(resp.json()['groups'])

def listAgentGroups(DEBUG,conn):
    print("\nAgent Group Name (Agent Group ID)")
    print("---------------------------------")
    for i in getAgentGroups(DEBUG,conn):
        print(str(i['name'])+" ("+str(i['id'])+")")


################################################################
# Start of program
################################################################
parser = argparse.ArgumentParser(description="Creates EKS environment to demonstration Tenable Container Security")
parser.add_argument('--debug',help="Display a **LOT** of information",action="store_true")
parser.add_argument('--listagents', help="Display all the agents.  Combine with --agentgroup to only show agents in that group.  Combine with --noagentgroup to show agents not in a group.",action="store_true",default=False)
parser.add_argument('--listagentgroups', help="Display all the agent groups.",action="store_true",default=False)
parser.add_argument('--agentgroup', help="Display all the agent groups.",nargs=1,action="store",default=[None])
parser.add_argument('--accesskey', help="Tenable.io access key.",nargs=1,action="store",default=[None])
parser.add_argument('--secretkey', help="Teanble.io secret key.",nargs=1,action="store",default=[None])
parser.add_argument('--noagentgroup', help="Display all the agent gropus.",action="store_true",default=False)
args = parser.parse_args()

DEBUG=args.debug
host="cloud.tenable.com"
port="443"

# Pull as much information from the environment variables about the system to which to connect
# Where missing then initialize the variables with a blank or pull from command line.
if os.getenv('TIO_ACCESS_KEY') is None:
    # If there is an access key specified on the command line, this override anything else.
    try:
        if args.accesskey[0] != "":
            accesskey = args.accesskey[0]
    except:
        accesskey=""
else:
    accesskey = os.getenv('TIO_ACCESS_KEY')



if os.getenv('TIO_SECRET_KEY') is None:
    # If there is an  secret key specified on the command line, this override anything else.
    try:
        if args.secretkey[0] != "":
            secretkey = args.secretkey[0]
    except:
        secretkey = ""

else:
    secretkey = os.getenv('TIO_SECRET_KEY')


conn = ConnectIO(DEBUG, accesskey, secretkey, host, port)

if conn == False:
    print("There was a problem connecting.")
    exit(-1)

print("Connection opened to Tenable.io")


if args.listagents:
    if DEBUG:
        print("Listing agents...")
    listAgents(DEBUG,conn,args.agentgroup[0],args.noagentgroup)

elif args.listagentgroups:
    if DEBUG:
        print("Listing agent groups...")
    listAgentGroups(DEBUG,conn)

exit(0)
