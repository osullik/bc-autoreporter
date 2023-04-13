import json, os

from parser import logEntryParser
from parser import inputHandler
from elasticConnector import openSearchConnector

listOfEntities = [	"HomerSimpson", 	"WaylonSmithers", 	"LennyLeonard", 
						"CarlCarlson", 		"MindySimmons", 	"FrankGrimes", 
						"CanaryMBurns", 	"Karl", 			"StuartDuck", 
						"Tibor", 			"Zutroy" ]

def updateSummaries(entity, summary):
	domain = 'bc23-autoreporter'
	host = 'search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com'
	region = "us-east-1"

	index_name = "employee_list"

	connector = openSearchConnector(domain,host,region)

	the_json = {"name":entity,
				"performance_summary":summary}

	connector.uploadDocument(index_name=index_name,observationJSON=the_json)

if __name__=="__main__":
	inputFiles = [("observations.txt", "MontgomeryBurns"),("observations_smithers.txt", "WaylonSmithers")]

	
	handler = inputHandler()
	parser = logEntryParser()

	docCounter = 0

	for (file,observer) in inputFiles:

		observations = handler.bulkImport(file)

		for observation in observations:

			if docCounter < 10:
				outFileName = "./output/observation_00"+str(docCounter)+".json"
			if docCounter >=10 and docCounter < 100:
				outFileName = "./output/observation_0"+str(docCounter)+".json"
			if docCounter >= 100:
				outFileName = "./output/observation_"+str(docCounter)+".json"


			dataDict = parser.convertLogToJSON(observation, listOfEntities, observer, "2021")
			
			#print(docCounter, file, observer,dataDict['entity'])


			with open(outFileName,"w") as f:								#Uncomment two lines below to create output for manual upload through dashbaord
				#f.write("PUT /observation-log/_doc/"+str(docCounter)+"\n")
				json.dump(dataDict,f)
				#f.write("\n")
			docCounter+=1

	filesToUpload = os.listdir("./summaries")
	
	for file in filesToUpload:
		intermediate = file.split("_")
		entity = intermediate[0]

		with open("./summaries"+"/"+file,"r") as f:
			summary = f.read()

		updateSummaries(entity,summary)


