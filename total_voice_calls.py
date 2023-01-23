#!/usr/bin/env python3

'''
This script is used to execute an snmpwalk to gather the total
numbers of calls on a CUBE router
'''
import sys
import os
import subprocess
from influxdb import InfluxDBClient
from datetime import datetime, timezone
import re

'''
*****************************************
*       Import Configuration File       *
*****************************************
'''
import config

#Time function to provided correctly formatted timestamp
def time():
	d = datetime.now(timezone.utc).astimezone()
	return str(d.isoformat())


#snmpwalk Command
cmd = f'snmpwalk -v 3 -a SHA -A {config.snmppasswd}  -l authPriv -u {config.snmpusr} -x AES -X {config.snmppasswd} {config.snmphost} 1.3.6.1.4.1.9.9.63.1.3.8.4.1.2.200'

#Execute snmpwalk command
try:
	output = os.popen(cmd).read()
except OSError:
	print ("Error: snmpwalk command did not execute correctly")
	print ("Exiting....")
	sys.exit()

#pull out needed value for totalCalls

totalCalls = ""
totalCalls = re.search(r"^.*Gauge32: (\d*)\s+", output, flags=re.DOTALL).group(1)
totalCalls = int(totalCalls)

'''
Now make connection to InfluxDB and post data
'''

client = InfluxDBClient(host=config.influxhost, port=8086)
client.switch_database('voice')

#JSON body format
json_body = [
	{
		"measurement": "totalCalls",
		"tags": {
			"source":"call-center"
		},
		"time":"{}".format(time()),
		"fields": {
			"totalCalls": totalCalls
		}
	}
]

#Write to InfluxDB
client.write_points(json_body)