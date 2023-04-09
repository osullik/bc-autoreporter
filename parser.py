
import os
import nltk
from nltk.tree import Tree
from nltk.metrics.distance  import edit_distance
import datefinder, datetime
from string import punctuation
import json
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Input Args:
#	reporter	-	string	-	The person reporting the observation
#	dtg			-	date	-	The Date Time Group of the report
#	logEntry 	-	string 	- 	A text description of an observation. 

# Actions: 
#	Parse Entities
#	Parse Date
#	Parse Tags
#	Sentiment Analysis	

# Outputs:
#	JSON Document to send to elasticsearch


class inputHandler():
	def __init__(self, inputType, fileName=None):
		self.inputType = inputType
		self.fileName = fileName
		self.parser = logEntryParser()

	def bulkImport(self):
		'''
		bulk import reads in a text file of observations. 
		Assumptions: 
			- Each log is on a new line
			- the Observations file is in the same directory. 
		Input (via Object):
			self.inputType - string - the type of ingest mode
			self.fileNmae - string - the name of the file to read logs from. 
		Output: 
			returns the contents of the file as a list of form ["<observation1>", "<observation2>"]
		'''

		observationList = []
		if self.inputType == "bulk":
			if self.fileName == None:
				print("Need to specify Filename")
			else:
				with open(self.fileName) as inputLog:
					observations = inputLog.readlines()

					for observation in observations:
						if observation.strip():
							observationList.append(observation)
				return observationList
		else: 
			print("Streaming input not implemented")



class logEntryParser():

	#def __init__():
	#	pass

	def parseEntities(self, logEntry, namedEntities):
		'''
		Extracts the target entities of the log entry

		Input Args: 
			logEntry - string - text of the log entry. 
			namedEntites - list of strinfs - the list of valid entites in the database
		Actions:
			- Tokenizes the log with naive whitespace splitting
			- Identifes entites with an @symbol prepended
			- Matches them to entities in the database with string distance
		Returns
			- The target entity from the database
		'''

		targetEntity = None 											# Initialize Vars		
		stringDistanceTolerance = 3										# User tunable Tolerance in string matching
		candidateList = []

		naiveTokenization = logEntry.split(' ')							# Tokenize based on whitespace

		for token in naiveTokenization:									# Loop through all tokens
			if token[0] == "@":											# Identify those starting with @
				candidateEntity = token[1:]								# Extract the likely entity 
				candidateList.append(candidateEntity)
																			#TODO - Early Stopping

				if candidateEntity in namedEntities:					# Check for exact entity matches
					targetEntity = candidateEntity
			
				else:													# Check for close misses (spelling errors)
					minDist = 1000
					likelyCandidate = None
					distList = []

					for entity in namedEntities:
						dist = edit_distance(candidateEntity.lower(), 
							entity.lower())
						distList.append((entity, dist))
						
						if dist < minDist:
							minDist = dist 
							likelyCandidate = entity

					if minDist < stringDistanceTolerance:				# Return the closest string with < a threshold of error
						targetEntity = likelyCandidate

				if targetEntity == None:
					targetEntity = "<UNKNOWN>_"+candidateEntity


		return targetEntity

	def parseDates(self, logEntry, defaultYear):	
		'''
		Function to extract dates from an employee observation log entry 
		Assumptions:
			1. All input dates are in US Format (MM/DD) when that is unclear
			2. The first date mentioned in the text is the correct date. 
		Known Bugs: 
			1. dateFinder will render 34 Feb 2021 as 21 Feb 2034
			2. dateFinder does not consistently apply MM/DD/YYYY format (day month confusion)
			3. dateFinder doesn't do well at finding dates in large text inputs (treated with token-fu belo)
		InputArgs: 
			logEntry - String - The text of the log entry 
			defaultYear - String - the year that will be used if no year is given 
		Actions: 
			Parse for dates
			Format in Elastic-compatible format
			Return first date mentioned in log
		Returns: 
			dateToReturn - String - YYYY/MM/DD format
		'''	

		dateToReturn = None

		months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", 
					"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

		defYear = datetime.datetime.strptime(defaultYear, "%Y")			# Define the default year to use (convert to date)	

		matches = list(datefinder.find_dates(logEntry, 					# Extract list of possible dates
											base_date=defYear))
		
		formattedMatches = []											# List to hold the string formatted dates


		if len(matches) > 0:											# Convert to YYYY/MM/DD formatted string
		    for date in matches:
		        formattedMatches.append(date.strftime('%Y-%m-%d'))

		    dateToReturn = formattedMatches[0]							# Return the first date mentioned in the text
		
		else: 
			tokens = nltk.word_tokenize(logEntry)						# Split string into tokens
			monthIndex = None
			candidateDate = "" 											

			for month in months: 										# Search all string for months 
				if monthIndex == None: 
					for token in tokens: 
						for month in months:
							if token.lower() ==month.lower():			# reduce errors from casing mismatch
								monthIndex = tokens.index(token)
								candidateDate+=(token)
								break
				else:
					break

				
				if monthIndex != None:									#I.e. if a month is found in the text

					strippedToken = tokens[monthIndex+1].strip("st") 	#Anchor on the month, check to see if day or year is next
					strippedToken = strippedToken.strip("nd")
					strippedToken = strippedToken.strip("rd")
					strippedToken = strippedToken.strip("th")
					if (strippedToken).isnumeric():
						candidateDate+=(" "+tokens[monthIndex+1])

					strippedNextToken = tokens[monthIndex+2].strip("st") #Anchor on the month, check to see if day or year is next
					strippedNextToken = strippedNextToken.strip("nd")
					strippedNextToken = strippedNextToken.strip("rd")
					strippedNextToken = strippedNextToken.strip("th")
					if (strippedNextToken).isnumeric():
						candidateDate+=(" "+tokens[monthIndex+2])

					if monthIndex != 0:
						strippedPriorToken = tokens[monthIndex-1].strip("st") #Anchor on the month, check to see if day or year is next
						strippedPriorToken = strippedPriorToken.strip("nd")
						strippedPriorToken = strippedPriorToken.strip("rd")
						strippedPriorToken = strippedPriorToken.strip("th")
						if (strippedPriorToken).isnumeric():
							candidateDate+=(" "+tokens[monthIndex-1])
						else:
							pass

			candidateMatch = list(datefinder.find_dates(candidateDate, 
														base_date = defYear))	# Convert the candidate date into a date object

			if len(candidateMatch) > 0:	
													# Convert to YYYY/MM/DD formatted string
				for date in candidateMatch:
					formattedMatches.append(date.strftime('%Y-%m-%d'))

				dateToReturn = formattedMatches[0]
				

			else:																#Handle situation where dates not detected in text or by Month anchoring
				for token in tokens:
					matches += list(datefinder.find_dates(token, 				# Extract list of possible dates
											base_date=defYear))
				formattedMatches = []											# List to hold the string formatted dates
				if len(matches) > 0:											# Convert to YYYY/MM/DD formatted string
				    for date in matches:
				        formattedMatches.append(date.strftime('%Y-%m-%d'))

				    dateToReturn = formattedMatches[0]							# Return the first date mentioned in the text


		return dateToReturn

	def parseTags(self, logEntry):
		'''
		ParseTags extracts the #tags from an employee log
		Input Args:
			logEntry - string - The emloyee log
		Actions: 
			- Naive Tokenization using whitespace delimiter
			- Look for tokens that start with a #
			- Append the terms to the list
		Outputs: 
			- tagList - list of strings of form ["Tag1", "Tag2"]
		Assumptions: 
			- No spaces in tags
		'''
		tagList = []
		naiveTokenization = logEntry.split(' ')							# Tokenize based on whitespace

		for token in naiveTokenization:									# Loop through all tokens
			token = token.lstrip()
			if len(token) >0:
				if token[0] == "#":											# Identify those starting with @
					candidateEntity = token[1:]								# Extract the likely entity 
					candidateEntity = candidateEntity.strip("\n")	# Strip newlines and other garbage
					candidateEntity = candidateEntity.strip(punctuation)	# Strip newlines and other garbage


																				#TODO - Early Stopping
					tagList.append(candidateEntity)
			else:
				pass

		return tagList

	# VADER (Valence Aware Dictionary and sEntiment Reasoner) is an open-source lexicon and rule-based sentiment analysis tool 
	# that is specifically attuned to sentiments expressed in social media.
	# Compound score is used to determine sentiment. It ranges from -1 (extreme negative) to +1 (extrememly positive)
	def sentiment_score(self, text):
  		sia = SentimentIntensityAnalyzer()
  		return sia.polarity_scores(text)['compound']


	# Function to return all adjectives and adverbs from the report text
	# Descriptive words (adjectives and adverbs) are most likely to influence the sentiment of the text.
	def extract_adj(self, text):
		tagged_text = nltk.pos_tag(text.split())
		return [i[0].strip(punctuation) for i in tagged_text if i[1] in ['RB','RBR','RBS','JJ','JJR','JJS']]  # adjectives or adverbs


	def convertLogToJSON(self, logEntry, entityList, observer, defaultYear="2021"):

		entity = self.parseEntities(logEntry, entityList)
		date = self.parseDates(logEntry, defaultYear)
		tagList = self.parseTags(logEntry)
		sentiment = self.sentiment_score(logEntry)
		adjectives = self.extract_adj(logEntry)

		dictToJSONify = {}

		dictToJSONify["entity"] = entity
		dictToJSONify["date"] = date
		dictToJSONify["tagList"] = tagList
		dictToJSONify["observation"] = logEntry
		dictToJSONify["sentiment"] = sentiment
		dictToJSONify["adjectives"] = adjectives
		dictToJSONify['observer'] = observer
		dictToJSONify['lastModified'] = (datetime.datetime.now()).strftime('%Y-%m-%dT%H:%M:%S')

		return dictToJSONify

		


