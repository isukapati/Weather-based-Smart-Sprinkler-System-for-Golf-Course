import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import urllib.request
import json
import requests
#Provide your IBM Watson Device Credentials
organization = "8unc2t"
deviceType = "Raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"


# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])

        if cmd.data['command']=='motoron':
                print("soil is dry, turned on the motor")
                
        elif cmd.data['command']=='motoroff':
                print("soil is wet, let the motor be turn off")
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        #To get the temp,hum data from weather a
        
        request_url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=Hyderabad,IN%20IN&appid=c6c3ed222a4661c01b50fda45f381b7c')
        print(request_url.read())

        soilmoisture = random.randrange(1,100)
        var=b'{"coord":{"lon":80.62,"lat":16.52},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"base":"stations","main":{"temp":39,"feels_like":45.33,"temp_min":39,"temp_max":39,"pressure":1004,"humidity":48},"visibility":6000,"wind":{"speed":1,"deg":110},"clouds":{"all":20},"dt":1590215792,"sys":{"type":1,"id":9207,"country":"IN","sunrise":1590192304,"sunset":1590239028},"timezone":19800,"id":1253184,"name":"Vijayawada","cod":200}'
        python=json.loads(var)
        print("...........temperature............")
        print("temp:", python['main']['temp'])
        print("humid:", python['main']['humidity'])
        temp=python['main']['temp']
        hum=python['main']['humidity']
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature': temp ,'Humidity': hum ,'soilmoisture': soilmoisture}
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum, "soilmoisture = %s %%" % soilmoisture, "to IBM Watson")

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if(soilmoisture<5):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=T9qVu185nf3kdKUatjOrxCvHGI7eMNByRA4iWlPLo2hgwE0QpZM3ixwoWDNcHRV6hv5G4SpKZy8uOXT0&sender_id=FSTSMS&message=Moisture Level Is Low.&language=english&route=p&numbers=9676563323')
        if not success:
                print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
