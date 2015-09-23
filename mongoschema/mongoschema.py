from pymongo import MongoClient
from collections import defaultdict
from prettytable import PrettyTable

class Schema(object):

	"Gets the schema of a MongoDB collection"
	
	DEFAULT_MONGO_URI = 'mongodb://localhost:27017/'
	DEFAULT_PORT = 27017

	def __init__(self, db_name, collection_name, where_dict={}, host=None, port=None, mongo_uri=DEFAULT_MONGO_URI, limit=0):
		"""
			Initializes Mongo Credentials given by user

			:param db_name: Name of the database
			:type  db_name: string

			:param collection_name: Name of the collection
			:type  collection_name: string

			:param where_dict: Filters (specific fields/value ranges etc.)
			:type  where_dict: dictionary

			:param host: Host IP
			:type  host: string

			:param port: Port number
			:type  port: int

			:param mongo_uri: Mongo Server and Port information
			:type  mongo_uri: string

			:param limit: Number of docs to be sampled
			:type  limit: int

		"""

		self.mongo_uri = mongo_uri
		self.db_name = db_name
		self.collection = collection_name
		self.where_dict = where_dict
		self.host = host
		self.port = port
		self.limit = limit


	def get_mongo_cursor(self):
		"""
			Returns Mongo cursor using the class variables

			:return: mongo collection for which cursor will be created
			:rtype: mongo colection object
		"""
		try:
			if self.host:
				if self.port:
					client = MongoClient(self.host, self.port)
				else:
					client = MongoClient(
						self.host, MongoCollection.DEFAULT_PORT)
			else:
				client = MongoClient(self.mongo_uri)

			db = client[self.db_name]
			cursor = db[self.collection]

			return cursor

		except Exception as e:
			msg = "Mongo Connection could not be established for Mongo Uri: {mongo_uri}, Database: {db_name}, Collection {col}, Error: {error}".format(
				mongo_uri=self.mongo_uri, db_name=self.db_name, col=self.collection, error=str(e))
			raise Exception(msg)

	

	def get_schema(self):
		"""
			Returns the schema related stats of a MongoDB collection
		"""
		cursor = self.get_mongo_cursor()
		result_set = cursor.find(self.where_dict).limit(self.limit)
		table = PrettyTable(['Key','Count','Percentage'])
		stat_dict = defaultdict(lambda: 0)
		type_dict = defaultdict(lambda: "")
		num_docs = 0

		for result in result_set:
			for key in result.keys():
				stat_dict[key] += 1
			num_docs += 1

		
		for k,v in stat_dict.iteritems():
			table.add_row([k,v,v*100/num_docs])

		print "Total number of docs:",num_docs
		print table


		








