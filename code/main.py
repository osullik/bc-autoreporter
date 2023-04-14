#Package Imports
import json
import argparse
import datetime

#MrFat Imports
from parser import logEntryParser
from parser import inputHandler
from elasticConnector import openSearchConnector

def updateSummaries(entity, summary):
	#ToDo: Remove Hard Coded Info
	domain = 'bc23-autoreporter'
	host = 'search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com'
	region = "us-east-1"

	index_name = "employee_list"

	connector = openSearchConnector(domain,host,region)

	the_json = {"name":entity,
				"performance_summary":summary}

	connector.uploadDocument(index_name=index_name,observationJSON=the_json)

class CliHandler():
	
	def __init__(self, inputArgs):
		self.inputArgs = inputArgs
		self.defaultYear = (datetime.datetime.today()).year
		
		#ToDo: Dynamicaly retrieve these from the database
		self.listOfEntities = [	"HomerSimpson", 	"WaylonSmithers", 	"LennyLeonard", 
								"CarlCarlson", 		"MindySimmons", 	"FrankGrimes", 
								"CanaryMBurns", 	"Karl", 			"StuartDuck", 
								"Tibor", 			"Zutroy" ]
		#print(self.inputArgs)

	def checkForErrors(self):
		'''
		Function to check the input args for inconsistent tag use and prevent errors from occuring. 
		'''
		detectedErrors = []

		if ((self.inputArgs["mode"] == "b" or self.inputArgs["mode"] == "bulk") and self.inputArgs["files"] == None):
			detectedErrors.append("Error: missing input file. Specify file with the -f or --file flags (e.g. -f inputfile.txt)")

		if ((self.inputArgs["mode"] == "s" or self.inputArgs["mode"] == "stream") and ("authKey" in self.inputArgs["creds"] or "secretKey" in self.inputArgs["creds"])):
			detectedErrors.append("Error: missing API credentials for stream. Specify with the -s or --stream flags (e.g. -s authkey secretkey)")

		if (("json" not in (self.inputArgs["output"]).lower()) and ("api" not in (self.inputArgs["output"]).lower())):
			detectedErrors.append("Error: incorrect output format specified. Use \'json\' or \'api\'")

		if ((self.inputArgs['mode'] not in ['b','bulk','s','stream','t', 'test'])):
			detectedErrors.append("Error: Invalid input mode. Select from [b, bulk, s, stream, t, test]")

		return detectedErrors

	def checkForWarnings(self):
		'''
		Function to check for bad practice and warn users
		'''
		detectedWarnings = []

		if ((self.inputArgs["mode"] != 'b' and self.inputArgs["mode"] != "bulk") and self.inputArgs["files"] != None):
			detectedWarnings.append("Warning: The files "+"".join(self.inputArgs['files'])+" will not be used outside of bulk import mode. Leave flag blank if not bulk importing")

		if ((self.inputArgs["mode"] != 's' and self.inputArgs["mode"] != "stream") and ("authKey" not in self.inputArgs["creds"] or "secretKey" not in self.inputArgs["creds"])):
			detectedWarnings.append("Warning: Streaming API credentials will not be used outside of streaming mode. Leave flag blank if not streaming")

		return(detectedWarnings)

	def generateInputTuples(self, inputFiles, observer="bulk_import"):
		'''
		Generates input tuples from the command line arguments to drive the ingestion of data in bulk
		Input args: 
			inputFiles - list - list of strings containing the names of files to be imported
			observer - string - the name of the person making the observation. Defaults to "bulk_import"
		Processes:
			create a tuple out of the two inputs
		Outputs: 
			inputTuples - tuple - of the form (filename, observer)
		'''
		observers = [None] * len(inputFiles)

		for x in range(0, len(inputFiles)):
			print(observer)
			observers[x] = observer

		inputTuples = list(zip(inputFiles,observers))

		return inputTuples

	def parseInputTuplesToDict(self, inputTuples):
		'''
		Reads in the files pushes them to the parser subsystem and creates a list of dictionaries for inputs
		Input Args: 
			inputTuples - tuples - of the form (filename, observer) where filename is the source of the observation and observer is the person making the entry
		processes: 
			Get the tuples, push to the input handler to import them, then the parser to get useful info out of them. Append to a list
		Output:
			inputObsList - list - a list of dictionaries in the shape of the opensearch database schema
		'''
		handler = inputHandler()
		parser = logEntryParser()

		docCounter = 0

		inputObsList = []

		for (file,observer) in inputTuples:

			observations = handler.bulkImport(file)

			dataDict = parser.convertLogToJSON(observation, self.listOfEntities, observer, self.defaultYear)

			inputObsList.append(dataDict)

		return inputObsList


	def outputObsDictToJSON(self, listofObsDicts):
		'''
		Formats the output files so that they can be read in through the python module that connects to opensearch
		Input Args: 
			listofObsDicts - List - List of dictionaries of the shape of the database scheme
		Processes:
			Dynamically Generate File names, fill each file with a single command, output files to output directory
		Outputs:
			Individual json files that can be pushed through the python opensearch functions to add data to the database programmatically. 
		'''

		for obsDict in listofObsDicts:

			for observation in observations:

				if docCounter < 10:
					outFileName = "./output/observation_00"+str(docCounter)+".json"
				if docCounter >=10 and docCounter < 100:
					outFileName = "./output/observation_0"+str(docCounter)+".json"
				if docCounter >= 100:
					outFileName = "./output/observation_"+str(docCounter)+".json"

			with open(outFileName,"w") as f:							
				json.dump(dataDict,f)
			docCounter+=1

	def outputObsDictToAPICommands(self, listofObsDicts):
		'''
		Formats the output files so that they can be read in through the opensearchAPI individually
		Input Args: 
			listofObsDicts - List - List of dictionaries of the shape of the database scheme
		Processes:
			Dynamically Generate File names, fill each file with a single command, output files to outputForAPI directory
		Outputs:
			Individual txt files that can be pushed to the API to add data to the database manually. 
		'''

		for obsDict in listofObsDicts:

			for observation in observations:

				if docCounter < 10:
					outFileName = "./outputForAPI/observation_00"+str(docCounter)+".txt"
				if docCounter >=10 and docCounter < 100:
					outFileName = "./outputForAPI/observation_0"+str(docCounter)+".txt"
				if docCounter >= 100:
					outFileName = "./outputForAPI/observation_"+str(docCounter)+".txt"

			with open(outFileName,"w") as f:								
				f.write("PUT /observation-log/_doc/"+str(docCounter)+"\n")
				json.dump(dataDict,f)
				f.write("\n")
			docCounter+=1




if __name__ =='__main__':

	argparser = argparse.ArgumentParser()									# initialize the argParser

	argparser.add_argument(	"-f", "--file", 								# command line triggers for streaming mode
							help="specifies the file(s) to be ingested for bulk import",
							nargs="+",			
							type=list,
							default=None,
							required=False)	

	argparser.add_argument(	"-m", "--mode", 								# command line triggers for the bulk import mode
							help="Define the mode of input from the following list (letter or word is valid): [b,bulk],[s,stream],[t,test]",		
							type=str,
							default='stream',
							required=True)									

	argparser.add_argument(	"-o", "--output", 								# command line triggers for the bulk import mode
							help="Specify the output type \'json\' or \'api\' ",		
							type=str, 
							default='json',
							required=False)	

	
	argparser.add_argument(	"-c", "--creds", 								# command line triggers for testing mode
							help="Creds for the twilio API used in streaming mode",
							nargs="*",
							type=list,			
							action='store',
							default=['authKey','secretKey'],
							required=False)
	
	
	flags = argparser.parse_args()											# populate variables from command line arguments

																			# Pull flags into dict (allows for easier testing)
	inputArgs = {}
	inputArgs["files"] = flags.file
	inputArgs["mode"] = flags.mode
	inputArgs["output"] = flags.output
	inputArgs["creds"] = flags.creds

	CH = CliHandler(inputArgs)

	errors = CH.checkForErrors()
	warnings = CH.checkForWarnings()

	if len(errors) > 0:
		print("ERRORS:")
		for error in errors:
			print(error)
		exit()
	else:
		if len(warnings) > 0:
			print("WARNINGS:")
			for warning in warnings:
				print(warning)

		inputTuples = CH.generateInputTuples(inputArgs['files'])
		listOfDicts = CH.parseInputTuplesToDict(inputTuples)

		if (inputArgs["output"]).lower() == 'json':
			CH.outputObsDictToJSON(listOfDicts)
		elif (inputArgs["output"]).lower() == 'api':
			CH.outputObsDictToAPICommands(listOfDicts)
		else:
			print("Error: Not able to recognise requested output format. Please try again using \'json\' or \'api\'")





