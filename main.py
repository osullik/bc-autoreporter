import json

from parser import logEntryParser
from parser import inputHandler

if __name__=="__main__":
	inputFiles = [("observations.txt", "MontgomeryBurns"),("observations_smithers.txt", "WaylonSmithers")]

	listOfEntities = [	"HomerSimpson", 	"WaylonSmithers", 	"LennyLeonard", 
						"CarlCarlson", 		"MindySimmons", 	"FrankGrimes", 
						"CanaryMBurns", 	"Karl", 			"StuartDuck", 
						"Tibor", 			"Zutroy" ]


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
			
			with open(outFileName,"w") as f:								#Uncomment two lines below to create output for manual upload through dashbaord
				#f.write("PUT /observation-log/_doc/"+str(docCounter)+"\n")
				json.dump(dataDict,f)
				#f.write("\n")
			docCounter+=1
