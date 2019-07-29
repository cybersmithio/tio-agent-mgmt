#!/usr/bin/python

import argparse
import re
from tenable_io.client import TenableIOClient


################################################################
# Start of program
################################################################
parser = argparse.ArgumentParser(description="Creates EKS environment to demonstration Tenable Container Security")
parser.add_argument('--debug',help="Display a **LOT** of information",action="store_true")
parser.add_argument('--listagents', help="Display all the agents.  Combine with --agentgroup to only show agents in that group.  Combine with --noagentgroup to show agents not in a group.",nargs=1,action="store_true",default=False)
parser.add_argument('--listgroups', help="Display all the agent gropus.",nargs=1,action="store",default=[None])
parser.add_argument('--agentgroup', help="Display all the agent gropus.",nargs=1,action="store",default=[None])
parser.add_argument('--noagentgroup', help="Display all the agent gropus.",action="store_true",default=False)
args = parser.parse_args()


DEBUG=args.debug

if args.listagents[0]:
    print("Listing agents.")
elif args.listgroups[0]:
    print("Listing agent groups.")


exit(0)
