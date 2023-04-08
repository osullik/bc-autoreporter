import json

from parser import logEntryParser
from parser import inputHandler

if __name__=="__main__":
	inputFile = "observations.txt"
	listOfEntities = [	"HomerSimpson", 	"WaylonSmithers", 	"LennyLeonard", 
						"CarkCarlson", 		"MindySimmons", 	"FrankGrimes", 
						"CanaryMBurns", 	"Karl", 			"StuartDuck", 
						"Tibor", 			"Zutroy" ]

	handler = inputHandler("bulk", inputFile)
	parser = logEntryParser()

	observations = handler.bulkImport()

	docCounter = 0
	for observation in observations:

		if docCounter < 10:
			outFileName = "./output/observation_00"+str(docCounter)+".json"
		if docCounter >=10 and docCounter < 100:
			outFileName = "./output/observation_0"+str(docCounter)+".json"
		if docCounter >= 100:
			outFileName = "./output/observation_"+str(docCounter)+".json"

		dataDict = parser.convertLogToJSON(observation, listOfEntities, "MontgomeryBurns", "2021" )
		
		with open(outFileName,"w") as f:
			json.dump(dataDict,f)
		docCounter+=1

