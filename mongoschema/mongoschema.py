import sys
import json
from pymongo import MongoClient
from collections import defaultdict
from prettytable import PrettyTable


class Schema(object):

    "Gets the schema of a MongoDB collection"

    DEFAULT_MONGO_URI = 'mongodb://localhost:27017/'

    def __init__(self, db_name, collection_name, where_dict={}, limit=0, mongo_uri=DEFAULT_MONGO_URI):
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

        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection = collection_name
        self.where_dict = where_dict
        self.limit = limit

    def get_mongo_cursor(self):
        """
            Returns Mongo cursor using the class variables

            :return: mongo collection for which cursor will be created
            :rtype: mongo colection object
        """
        try:
            client = MongoClient(self.mongo_uri)
            db = client[self.db_name]
            cursor = db[self.collection]
            return cursor
        except Exception as e:
            msg = "Mongo Connection could not be established for Mongo Uri: {mongo_uri}, Database: {db_name}, Collection {col}, Error: {error}".format(
                mongo_uri=self.mongo_uri, db_name=self.db_name, col=self.collection, error=str(e))
            raise Exception(msg)

    def get_pretty_table(self, key_type_count):
        """
            Returns PrettyTable object built using the key_type dictionary

            :param key_type_count: The distribution of key types
            :type key_type_count: dictionary

            :return: PrettyTable built from the key type dict
            :rtype: PrettyTable object

        """
        pretty_table_defaul_value = [
            'Key', 'Occurrence Count', 'Occurrence Percentage', 'Values Type', 'Value Type Percentage']
        result_table = PrettyTable(pretty_table_defaul_value)

        for key, key_types in key_type_count.iteritems():
            max_key_type_count = max(key_types.values())
            max_key_type = [key_type for key_type, key_type_count in key_types.iteritems(
            ) if key_type_count == max_key_type_count][0]

            if key_types['total']:
                max_key_percent = round(
                    max_key_type_count * 100.0 / key_types['total'], 2)
            else:
                max_key_percent = 0.00

            occurrence_percent = round(
                key_types['total'] * 100.0 / total_docs, 2)
            prettytable_row = [
                key, key_types['total'], occurrence_percent, max_key_type, max_key_percent]
            result_table.add_row([key, v, v * 100 / num_docs])

        return result_table

    def get_schema(self):
        """
                Returns the schema related stats of a MongoDB collection

                :return: total number of docs and PrettyTable
                :rtype: int and PrettyTable object

        """
        total_docs = 0
        key_type_count_default_value = {
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
            "other": 0,
            "total": 0
        }

        cursor = self.get_mongo_cursor()
        if self.limit:
            mongo_collection_docs = cursor.find(
                self.where_dict).limit(self.limit)
        else:
            mongo_collection_docs = cursor.find(self.where_dict)

        key_type_count = defaultdict(lambda: key_type_count_default_value)

        for doc in mongo_collection_docs:
            for key in doc.keys():
                key_type_count[key]["total"] += 1
                if type(key) in key_type_count[key].keys():
                    key_type_count[key][type(key)] += 1
                else:
                    key_type_count[key]["other"] += 1
            total_docs += 1

        result_table = get_pretty_table(key_type_count)
        return total_docs, result_table


def main():

    mongo_uri = str(raw_input(
        'Please Provide the MONGO_URI, Press Enter for the Default MONGO_URI '))
    db_name = str(raw_input('Please Provide the Database Name '))
    collection_name = str(raw_input('Please Provide the Collection Name '))
    where_dict = str(
        raw_input('Please Provide the Filter dictionary, Press Enter for None '))
    limit = str(raw_input(
        'Please Provide the Number of Docs to be analyzed, Press Enter for all the docs '))

    if not limit:
        limit = 0
    else:
        limit = int(limit)

    if not where_dict:
        where_dict = {}
    else:
        where_dict = json.loads(where_dict)

    if mongo_uri:
        schema_obj = Schema(
            db_name, collection_name, where_dict, limit, mongo_uri)
    else:
        schema_obj = Schema(db_name, collection_name, where_dict, limit)

    if mongo_uri and limit and where_dict:
        schema_obj = Schema(
            db_name, collection_name, where_dict, limit, mongo_uri)

    total_docs, result_table = schema_obj.get_schema()
    print "Total Number of Documents: " + str(total_docs)
    print result_table

if __name__ == '__main__':
    main()
