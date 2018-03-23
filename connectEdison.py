# For edisonClient
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient as AWSIoT

# For edisonShadow
#from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient as IoTSHADOW

import logging     # For debugging
import json        # For JSON payload
import time

#==============================================================================
'''
PURPOSE : Custom MQTT message callback
'''
def customCallback(client, userdata, message):
	print("Received a new message: ")
	print(message.payload)
	print("from topic: ")
	print(message.topic)
	print("--------------\n\n")

#==============================================================================
'''
PURPOSE : Custom Shadow callback
           - payload is the JSON message to be sent to update shadow
           - responseStatus can be timeout, accepted, rejected
           - token is present only if a client token was used when published valid JSON
             to the "/update" topic.
'''
def customShadowCallback_Update(payload, responseStatus, token):
	# payload is a JSON string ready to be parsed using json.loads(...)
	# in both Py2.x and Py3.x
	if responseStatus == "timeout":
		print("Update request " + token + " time out!")
	if responseStatus == "accepted":
		payloadDict = json.loads(payload)
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Update request with token: " + token + " accepted!")
		print("welcome: " + str(payloadDict["state"]["desired"]["welcome"]))
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Update request " + token + " rejected!")

#==============================================================================
'''
PURPOSE : Function to delete JSON payload state

'''
def customShadowCallback_Delete(payload, responseStatus, token):
	if responseStatus == "timeout":
		print("Delete request " + token + " time out!")
	if responseStatus == "accepted":
		print("~~~~~~~~~~~~~~~~~~~~~~~")
		print("Delete request with token: " + token + " accepted!")
		print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
	if responseStatus == "rejected":
		print("Delete request " + token + " rejected!")

#==============================================================================
'''
# PURPOSE - Store Edison endpoint
# NOTE    - This is found in the AWS IoT platform under your device,
# 			and I believe under the "Interact" tab.
'''
edisonEndpoint = ("ab68ecxhb4vux.iot.us-east-2.amazonaws.com")

'''
# PURPOSE - Used for the client name and the topic name.
# NOTE 	  - In the IoT platform, I named my Edison board "spawarEdison"
#		    which means that this will also be the name of the topic
#			that I will be publishing to.
'''
client = ("jbox001")


'''
# PURPOSE - Store credentials in variables for easier reference.
# NOTE 	  - These are the filepaths as they are stored on the Intel Edison.
'''
rootCA = ("rootCA.pem.crt")
privateKey = ("private.pem.key")
cert = ("cert.pem.crt")

'''
# PURPOSE - Configure logging to see line-by-line output when you
#		    ssh into the Edison and test your code.
# NOTE 	  - DEBUG is for robust output. Change DEBUG to ERROR to see
#		    less output when you ssh into the Edison.
'''
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - \n\t%(name)s - \n\t%(levelname)s - \n\t%(message)s\n')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

'''
# PURPOSE - Initialize the Intel Edison Client as an AWS IoT MQTT Client
# NOTE 	  - I import the AWSIoTMQTTClient as AWSIoT for less typing.
'''
#Initialize AWSIoTMQTTClient
edisonClient = None
edisonClient = AWSIoT(client)

#==============================================================================
'''
PURPOSE - Function to connect to AWS IoT
NOTE    - MQTT is on port 8883
'''
def establishConnection():
     # Configure endpoints and credentials
     edisonClient.configureEndpoint(edisonEndpoint, 8883)
     edisonClient.configureCredentials(rootCA, privateKey, cert)

     # Configure edisonClient connection
     edisonClient.configureAutoReconnectBackoffTime(1, 32, 20)
     edisonClient.configureOfflinePublishQueueing(-1)
     edisonClient.configureDrainingFrequency(2)
     edisonClient.configureConnectDisconnectTimeout(10)
     edisonClient.configureMQTTOperationTimeout(5)

     # Connect to AWS IoT
     edisonClient.connect()

#==============================================================================
'''
PURPOSE - Function to unsubscribe from a topic and disconnect from AWS IoT
'''
def disconnect():
     # Unsubscribe from topic
     edisonClient.unsubscribe(client)

     # Disconnect from AWS IoT
     print("spawarEdison is now disconnecting.....")
     edisonClient.disconnect()

#==============================================================================
'''
PURPOSE - Function to subscribe to topic
'''
def subscribe(myTopic):
     edisonClient.subscribe(myTopic, 1, customCallback)
     time.sleep(3)

#==============================================================================
'''
PURPOSE - Function to publish to a topic in a loop
'''
def publish(edisonTopic):
     loopCount = 0

	 # Publish in a loop 5 times
     while loopCount < 5:
		 # Store separate messages for efficiency
         iphoneMessage = '{"default": "This is default message","APNS": "{\"aps\":{\"alert\": \"iPhone says...Check out these awesome deals!\",\"url\":\"www.amazon.com\"} }"}'
         emailMessage = '{"default": "This is default message","email": "I am sending an email"}'
         emailJSONMessage = '{"default": "Hello","email-json":"I am sending JSON email message"}'
         httpMessage = '{"default": "Hello World", "http":"This is the http message"}'
         httpsMessage = '{"default":"Bye", "https":"This is secured HTTP message"}'

		 # Publish the messages to the edison topic
         edisonClient.publish(edisonTopic, iphoneMessage + str(loopCount), 1)
         edisonClient.publish(edisonTopic, emailMessage + (str(loopCount) * 2), 1)
         edisonClient.publish(edisonTopic, emailJSONMessage + (str(loopCount) * 3), 1)
         edisonClient.publish(edisonTopic, httpMessage, 1)
         edisonClient.publish(edisonTopic, httpsMessage, 1)

         # Publish to SNS Topic using ARN
         edisonClient.publish("arn:aws:sns:us-east-2:541776619006:edison-SNS-001", emailMessage, 1)

		 loopCount += 1
         time.sleep(3)

#==============================================================================
'''
PURPOSE - For simplicity, and only need to call this function to initiate the
          proper sequence of events
'''
def driver():
     establishConnection() # Connect
     subscribe(client)	   # Subscribe
     publish(client)       # Publish
     disconnect()		   # Unsubscribe and Disconnect

#==============================================================================
'''
PURPOSE - Call driver to run program, which will be easier if scaled up
'''
driver()


# =====================     END FILE     =====================================
