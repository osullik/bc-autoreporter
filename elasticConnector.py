import elasticsearch
from datetime import datetime

class elasticConnector():
	def __init__(url, username, password):
		print("Initialized elasticConnector Class")

		self.url = url
		self.username = username
		self.password = password

		self.client = Elasticsearch()