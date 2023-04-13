from twilio.rest import Client
from elasticConnector import openSearchConnector
from streamingInput import streamingInputHandler
import datetime, pytz
import time


class twillioConnector():

	def __init__(self, index):

		# Your Account SID from twilio.com/console
		#self.account_sid = "SID_here"
		# Your Auth Token from twilio.com/console
		#self.auth_token  = "auth_tokenHere"


		self.index = index

		self.client = Client(self.account_sid, self.auth_token)

		self.domain = 'bc23-autoreporter'
		self.host = 'search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com'
		self.region = "us-east-1"
		self.connector = openSearchConnector(self.domain,self.host,self.region)
		self.streamer = streamingInputHandler(self.index, "./logs")

		self.startTime = datetime.datetime.now()

		utc=pytz.UTC

		print("startTime is", utc.localize(self.startTime))




	def getMessages(self):
		mostRecent = self.getMostRecent(self.index)
		utc=pytz.UTC
		messageList = []

		for sms in self.client.messages.list():
			if sms._from == "whatsapp:+61431133963":
				#print(sms.date_sent, utc.localize(datetime.datetime.strptime(mostRecent, '%Y-%m-%dT%H:%M:%S')))
				if sms.date_sent.replace(tzinfo=pytz.utc) < (self.startTime).replace(tzinfo=pytz.utc):
					pass
				else:
					messageList.append((sms._from, sms.body))

		return messageList


	def getMostRecent(self,index):		
		query = {
				  "query": {
				    "match_all": {}
				  },
				  "size": 1,
				  "sort": [
				    {
				      "lastModified": {
				        "order": "desc"
				      }
				    }
				  ]
				}

		mostRecentRecord = self.connector.search.search(body=query, index=index)
		mostRecent = mostRecentRecord["hits"]["hits"][0]["_source"]["lastModified"]
		self.mostRecent = mostRecent

		return mostRecent



if __name__=="__main__":
	tc = twillioConnector("obs2")

	while True:

		mostRecent = tc.getMostRecent("obs2")

		messages = tc.getMessages()

		if len(messages) == 0:
			print("No new messages")
		else:

			for (origin, comment) in messages:
				tc.streamer.processStreamInput(inputText=comment, observer=origin)

		time.sleep(20)
		print("Fetching new Messages")