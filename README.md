# mongoschema
**MongoDB schema information in Python**

**mongoschema** is a library written in Python to provide concise description of the schema of a collection in MongoDB



## Installation
***
To install the package, type the following -

	pip install mongoschema


## Sample data - Populating MongoDB with sample data
***
Navigate to `test/sample_data` in the `mongojoin` directory and type the following command -

	> mongoimport --dbname test --collection supplier --file supplier.json
	> mongoimport --dbname test --collection order --file order.json

This will create and populate the required collections with sample data.


The two collections *supplier* and *order* will be used to demonstrate how to use **mongoschema**.
To check the contents of the collection, the following command can be used in the MongoDB shell :

	> use test
	> db.supplier.find({})
	> db.order.find({})

## Using `mongoschema` to get the schema information of a MongoDB collections
***
Type the following in Python shell to import `mongoschema`- 

	>>> from mongoschema import Schema

To create a `Schema` object for the collection to be analysed, type the following -

	>>> schema = Schema("test", "supplier")

where `test` is the DB name and `supplier` is the Collection name.


Additional parameters -
`host` : Mongo uri (String)
`port` : Port Number (Integer)
`limit`: Number of docs to be sampled

To get the stats of the collection -

	>>> num_docs, result = schema.get_schema()

`num_docs`: Total number of docs sampled
`result`  : Dictionary containing the stats

Use the following command to pretty print the results -

    >>> schema.print_schema()


    +-------------+------------------+-----------------------+------------------+-----------------------+
	|   Key       | Occurrence Count | Occurrence Percentage |    Value Type    | Value Type Percentage |
	+-------------+------------------+-----------------------+------------------+-----------------------+
	| supplier_id |        7         |         100.0         |   <type 'int'>   |         100.0         |
	|     name    |        7         |         100.0         | <type 'unicode'> |         100.0         |
	|     _id     |        7         |         100.0         |      other       |         100.0         |
	+-------------+------------------+-----------------------+------------------+-----------------------+

More contents here - https://pypi.python.org/pypi/mongoschema/
