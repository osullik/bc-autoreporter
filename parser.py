
import os
import nltk
from nltk.tree import Tree
from nltk.metrics.distance  import edit_distance
import datefinder, datetime
import re

'''
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
'''

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

		naiveTokenization = logEntry.split(' ')							# Tokenize based on whitespace

		for token in naiveTokenization:									# Loop through all tokens
			if token[0] == "@":											# Identify those starting with @
				candidateEntity = token[1:]								# Extract the likely entity 
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

		print(logEntry)
		dateToReturn = None

		months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December", 
					"Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

		defYear = datetime.datetime.strptime(defaultYear, "%Y")			# Define the default year to use (convert to date)	

		matches = list(datefinder.find_dates(logEntry, 					# Extract list of possible dates
											base_date=defYear))
		
		print(matches)
		formattedMatches = []											# List to hold the string formatted dates

		if len(matches) > 0:											# Convert to YYYY/MM/DD formatted string
		    for date in matches:
		        formattedMatches.append(date.strftime('%Y/%m/%d'))

		    dateToReturn = formattedMatches[0]							# Return the first date mentioned in the text
		
		else: 
			tokens = nltk.word_tokenize(logEntry)						# Split string into tokens
			monthIndex = None
			candidateDate = "" 											

			for month in months: 										# Search all string for months 
				if monthIndex == None: 
					for token in tokens: 
						if token in months:
							monthIndex = tokens.index(token)
							candidateDate+=(token)
							break
				else:
					break

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

			candidateMatch = list(datefinder.find_dates(candidateDate))			# Convert the candidate date into a date object

			if len(candidateMatch) > 0:											# Convert to YYYY/MM/DD formatted string
				for date in candidateMatch:
					formattedMatches.append(date.strftime('%Y/%m/%d'))

				dateToReturn = formattedMatches[0]

		return dateToReturn


