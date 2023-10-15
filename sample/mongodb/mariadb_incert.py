# モジュールをインポート
import csv

import dateutil.parser
from pymongo import MongoClient

# Connect to MongoDB
# client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient("mongodb://admin:[pw]@localhost:27017/")
client = MongoClient("mongodb://mac001:001mac@localhost:27017/")
# Select DB
db = client.ec_sol_db1
# Select a collection
collection = db.ec_sol_pes_tbl

# Open CSV file
with open("data.csv", "r") as f:
    # Create CSV reader
    reader = csv.reader(f)
    # Create a list of documents
    docs = []
    # Create a list of column names (for example, name them col1 through col55)
    col_names = ["col" + str(i) for i in range(1, 56)]
    # For each row of the CSV file
    for row in reader:
        # Create documentation
        doc = {}
        # Match column names to values and add to document
        for col_name, value in zip(col_names, row):
            # Convert to float if value is numeric
            try:
                value = float(value)
            # Convert to Date type if the value is a date
            except ValueError:
                try:
                    value = dateutil.parser.parse(value)
                # If the value is a string, leave it as it is.
                except ValueError:
                    pass
            # Add to documentation
            doc[col_name] = value
        # Add to list of documents
        docs.append(doc)
    # Run bulk insert
    collection.insert_many(docs)
