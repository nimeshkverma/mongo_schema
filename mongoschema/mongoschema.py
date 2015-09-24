import sys
import json
from pymongo import MongoClient
from collections import defaultdict
from prettytable import PrettyTable


class Schema(object):

    "Gets the schema of a MongoDB collection"

    DEFAULT_MONGO_URI = 'mongodb://localhost:27017/'
    DEFAULT_PORT = 27017

    def __init__(self, db_name, collection_name, where_dict={}, limit=0, mongo_uri=DEFAULT_MONGO_URI, host=None, port=None):
        """
                Initializes Mongo Credentials given by user

                :param db_name: Name of the database
                :type  db_name: string

                :param collection_name: Name of the collection
                :type  collection_name: string

                :param where_dict: Filters (specific fields/value ranges etc.)
                :type  where_dict: dictionary

                :param mongo_uri: Mongo Server and Port information
                :type  mongo_uri: string

                :param limit: Number of docs to be sampled
                :type  limit: int

        """

        self.db_name = db_name
        self.collection = collection_name
        self.where_dict = where_dict
        self.limit = limit
        self.mongo_uri = mongo_uri
        self.host = host
        self.port = port

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

    def get_pretty_table(self, key_type_count, total_docs):
        """
                Returns PrettyTable object built using the key_type dictionary

                :param key_type_count: The distribution of key types
                :type key_type_count: dictionary

                :return: PrettyTable built from the key type dict
                :rtype: PrettyTable object

        """
        pretty_table_headers = [
            'Key', 'Occurrence Count', 'Occurrence Percentage', 'Value Type', 'Value Type Percentage']
        result_table = PrettyTable(pretty_table_headers)
        
        for key, key_types in key_type_count.iteritems():


            max_key_type_count = sorted(key_types.values())[-2]
            max_key_type = [key_type for key_type, key_type_count in key_types.iteritems(
            ) if key_type_count == max_key_type_count][0]

            max_key_percent = round(max_key_type_count * 100.0 / key_types['total'], 2) if key_types['total'] else 0.0

            occurrence_percent = round(key_types['total'] * 100.0 / total_docs, 2)

            prettytable_row = [key, key_types['total'], occurrence_percent, max_key_type, max_key_percent]
            result_table.add_row(prettytable_row)

        return result_table

    def get_schema(self):
        """
                        Returns the schema related stats of a MongoDB collection

                        :return: total number of docs and PrettyTable
                        :rtype: int and PrettyTable object

        """
        total_docs = 0
        key_type_default_count = {
            int: 0,
            float: 0,
            str: 0,
            bool: 0,
            dict: 0,
            list: 0,
            set: 0,
            tuple: 0,
            None: 0,
            object: 0,
            unicode:0,
            "other": 0,
            "total": 0
        }

        cursor = self.get_mongo_cursor()
        mongo_collection_docs = cursor.find(
            self.where_dict).limit(self.limit)

        key_type_count = defaultdict(lambda: key_type_default_count)

        for doc in mongo_collection_docs:
            for key, value in doc.iteritems():
                key_type_count[key]["total"] += 1
                if type(value) in key_type_count[key].keys():
                    key_type_count[key][type(value)] += 1
                else:
                    key_type_count[key]["other"] += 1
            total_docs += 1

        result_table = self.get_pretty_table(key_type_count, total_docs)
        return total_docs, result_table

    def print_schema(self):
        """
                Prints the schema related stats of a MongoDB collection
        """

        total_docs, result_table = self.get_schema()

        print "Total number of docs : {total_docs}".format(total_docs=total_docs)
        print result_table
