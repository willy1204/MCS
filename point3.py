#!/usr/bin/python

import Adafruit_DHT
import time
import sys
import httplib
import urllib
import json
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_UP)
deviceId = "Dfr3Iwyb"
deviceKey = "ErJQU4MNQGwLnthh"
def post_to_mcs(payload):
        headers = {"Content-type": "application/json", "deviceKey": deviceKey}
        not_connected = 1
        while (not_connected):
                try:
                        httpClient = httplib.HTTPConnection("api.mediatek.com:80")
                        httpClient.connect()
			not_connected = 0
                except (httplib.client.HTTPException, socket.error) as ex:
                        print ("Error: %s" % ex)
                        time.sleep(10)
                         # sleep 10 seconds
        httpClient.request("POST", "/mcs/v2/devices/" + deviceId + "/datapoints",json.dumps(payload), headers)
        response = httpClient.getresponse()
        print( response.status, response.reason, json.dumps(payload), time.strftime("%c"))
        data = response.read()
        httpClient.close()
while True:
 	SwitchStatus = GPIO.input(26)
        if SwitchStatus == 0:
               print('Button pressed')
        else:
               print('Button released')
 	payload = {"datapoints":[{"dataChnId":"SwitchStatus","values":{"value":SwitchStatus}}]}
        post_to_mcs(payload)
        time.sleep(2)
