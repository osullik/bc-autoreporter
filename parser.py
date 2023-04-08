
import os

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

	def __init__(reporter, dtg, logEntry):
		pass
