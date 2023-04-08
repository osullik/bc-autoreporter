
import os
import nltk
from nltk.tree import Tree
from nltk.metrics.distance  import edit_distance

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
