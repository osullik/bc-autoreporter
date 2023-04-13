from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from requests_aws4auth import AWS4Auth
import boto3
from datetime import datetime
import os
import json
from summarizer import Summarizer
#from urllib.error import HTTPError

class openSearchConnector():

	def __init__(self, domainName, host, region):
		#To make this work you need to set up amazon CLI
		#do Amazon Configure on cli and enter the keys you generate at AWS IAM portal
		self.os_client = boto3.client("opensearch")
		self.description = self.os_client.describe_domain(DomainName=domainName)
		self.host = host # For example, my-test-domain.us-east-1.es.amazonaws.com
		self.region = region # e.g. us-west-1

		self.service = 'es'
		self.credentials = boto3.Session().get_credentials()			#Note for this to work you need to have AWS CLI configured on your system with keys installed
		self.awsauth = AWS4Auth(self.credentials.access_key, 
									self.credentials.secret_key, 
									self.region, 
									self.service, 
									session_token=self.credentials.token)

		self.search = OpenSearch(
		    hosts = [{'host': host, 'port': 443}],
		    http_auth = self.awsauth,
		    use_ssl = True,
		    verify_certs = True,
		    connection_class = RequestsHttpConnection
		)

	def deleteIndex(self,index_name):
		self.search.indices.delete(index_name)	#index Destructor
		print(index_name, "Deleted")

	def createIndex(self, index_name):
		'''
		Creates an index of a given name
		Input Args:
			index_name - string - name for the index
		Returns:
			Null
		'''
													#indexSchema defines the Settings and Mappings
		indexSchema = {				
					  "settings": {
					    "index": {
					      "number_of_shards": 1,
					      "number_of_replicas": 1
					    }
					  },
					  "mappings": {
						  "properties": {
						    "adjectives": {
						      "type": "keyword"
						    },
						    "date": {
						      "type": "date"
						    },
						    "entity": {
						      "type": "text"
						    },
						    "lastModified": {
						      "type": "date"
						    },
						    "observation": {
						      "type": "text"
						    },
						    "observer": {
						      "type": "text"
						    },
						    "sentiment": {
						      "type": "integer"
						    },
						    "tagList": {
						      "type": "keyword"
						    }
						  }
						}
					}
		self.search.indices.create(index_name, body=indexSchema)	#index Constructor

	def uploadDocument(self, index_name, observationJSON):

		#TODO: Check if document exists

		self.search.index(index_name, body=observationJSON)

	def bulkUpload(self, dataSource, index_name):

		filesToUpload = os.listdir(dataSource)
		for file in filesToUpload:
			with open(dataSource+"/"+file) as f:
				jsonToUpload = json.load(f)
			self.uploadDocument(index_name,jsonToUpload)

	def searchByName(self,idx,name):

		# Size is a big number here since we're doing exact matching, take the risk
		query = {
		  'size': 100,
		  'query': {
		    'multi_match': {
		      'query': name,
		      'fields': ['entity']
		    }
		  }
			}
		results = self.search.search(body=query,index=idx)
		return(results)

		
if __name__=="__main__":
	domain = 'bc23-autoreporter'
	host = 'search-bc23-autoreporter-4ob7m4onu2evrdqghxxcfoo6cu.us-east-1.es.amazonaws.com'
	region = "us-east-1"

	index_name = "obs2"
	osc = openSearchConnector(domain,host, region)

	try:
		osc.deleteIndex("obs2")
	except:
		print("couldnt delete")

	osc.createIndex("obs2")

	#with open('./output/observation_000.json') as jsonFile:
	#	singleJSON = json.load(jsonFile)

	#osc.uploadDocument("obs2", singleJSON)

	osc.bulkUpload("./output", index_name)
	
	'''
	#code to generate the summaries of text
	listOfEntities = [	"HomerSimpson", 	"WaylonSmithers", 	"LennyLeonard", 
						"CarlCarlson", 		"MindySimmons", 	"FrankGrimes", 
						"CanaryMBurns", 	"Karl", 			"StuartDuck", 
						"Tibor", 			"Zutroy" ]

	for entity in listOfEntities:
		print("Generating Summary of", entity)

		results = osc.searchByName(index_name, entity)
		listOfDicts = []
		for result in results["hits"]["hits"]:
			listOfDicts.append(result["_source"])

		sumer = Summarizer()
		output = (sumer.employee_summarize(listOfDicts))

		with open("./"+entity+"_summary.txt",'w') as f:
			f.write(output)
	'''


