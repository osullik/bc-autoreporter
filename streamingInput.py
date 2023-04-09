import json
import datetime
import nltk
import os

from parser import logEntryParser
from parser import inputHandler
from elasticConnector import openSearchConnector

class streamingInputHandler():

	def __init__(self, indexName, logDirectory):

		domain = 'bc23-autoreporter'
		host = 'search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com'
		region = "us-east-1"

		self.index_name = indexName

		self.parser = logEntryParser()
		self.handler = inputHandler()									#Not really required, designed for bulk ingest
		self.connector = openSearchConnector(domain, host, region)
		self.logDirectory = logDirectory
		self.logFile = logDirectory+"/log.txt"

		self.entityList = [	"HomerSimpson", 	"WaylonSmithers", 	"LennyLeonard", 
							"CarlCarlson", 		"MindySimmons", 	"FrankGrimes", 
							"CanaryMBurns", 	"Karl", 			"StuartDuck", 
							"Tibor", 			"Zutroy" ]

		self.defaultYear = "2021"

		if os.path.exists(self.logDirectory) == False:
			os.makedirs(self.logDirectory)

		if os.path.exists(self.logFile) == False:
			with open(self.logFile, "x") as f:
				f.write("Log commenced: "+str(datetime.datetime.now())+"\n")

	def processStreamInput(self,inputText, observer):

		parsedLogAsDict = self.parser.convertLogToJSON(inputText, self.entityList, observer, self.defaultYear)

		if self.connector.search.indices.exists(self.index_name) == True:
			pass 
		else:
			self.connector.createIndex(self.index_name)


		#assume since streaming all observations are unique

		jsonToPush = json.dumps(parsedLogAsDict)

		print(jsonToPush)

		self.connector.uploadDocument(index_name=self.index_name,observationJSON=jsonToPush)

		#Log for record keeping
		with open(self.logFile, "a") as log:
			log.write(str(datetime.datetime.now()) + " report from "+parsedLogAsDict['observer']+" about "+parsedLogAsDict['entity']+" has been pushed to "+ self.index_name+"\n") 

		with open(self.logDirectory+"/"+str(datetime.datetime.now())+"_obs_"+parsedLogAsDict['observer']+"_"+parsedLogAsDict['entity'], "w") as record:
			json.dump(parsedLogAsDict,record)


if __name__=="__main__":
	streamer = streamingInputHandler("streamlogs","./logs")

	streamInput1 = "@FrankGrimes was observed to have continued conflict with @HomerSimpson. \
	Despite being assigned to work together on a task, the two were unable to collaborate effectively and frequently argued \
	over the best approach. Frank's frustration with Homer's perceived laziness and incompetence led to tension and decreased productivity. \
	#Collaboration #Conflict #Productivity"

	streamInput2 = "On June 29th @HomerSimpson was observed to perform to a satisfactory standard. \
	This was evidenced by his willingness to work on a holiday in order to assist with an important project. \
	His actions show #dedication and #teamwork."

	streamInput3 = "On October 14th, 2021, @WaylonSmithers was observed to perform to an excellent standard. \
	This was evidenced by his management of a crisis situation, which required quick thinking and decisive action. \
	His actions show #resilience #problem-solving #leadership."

	streamer.processStreamInput(streamInput1, "HiredGoons")

	streamer.processStreamInput(streamInput2, "LarryBurns")

	streamer.processStreamInput(streamInput3, "Blinky")






# Process it to json

# Push it to DB