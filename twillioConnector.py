from twilio.rest import Client
from elasticConnector import openSearchConnector
from streamingInput import streamingInputHandler
import datetime, pytz


class twillioConnector():

	def __init__(self, index):

		# Your Account SID from twilio.com/console
		self.account_sid = "AC1b5439222dada3f7f8669e653d59e8cf"
		# Your Auth Token from twilio.com/console
		self.auth_token  = "e3e164962c8841828e30060d339c6f47"


		self.index = index

		self.client = Client(self.account_sid, self.auth_token)

		self.domain = 'bc23-autoreporter'
		self.host = 'search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com'
		self.region = "us-east-1"
		self.connector = openSearchConnector(self.domain,self.host,self.region)
		self.streamer = streamingInputHandler(self.index, "./logs")




	def getMessages(self):
		print("Get em")
		mostRecent = self.getMostRecent(self.index)
		utc=pytz.UTC

		messageList = []

		for sms in self.client.messages.list():
			if sms._from == whatsapp:"+61431133963":
				if sms.date_sent < utc.localize(datetime.datetime.strptime(mostRecent, '%Y-%m-%dT%H:%M:%S')):
					pass
				else:
					messageList.append((sms._from, sms.body))

		return messageList


	def getMostRecent(self,index):
		print("most Recent")
		
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
		
		return mostRecent


if __name__=="__main__":
	print("Start")
	tc = twillioConnector("obs2")

	mostRecent = tc.getMostRecent("obs2")

	messages = tc.getMessages()

	for (origin, comment) in messages:
		tc.streamer.processStreamInput(inputText=comment, observer=origin)