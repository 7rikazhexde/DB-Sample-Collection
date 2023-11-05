from decimal import Decimal, InvalidOperation

import boto3
import pandas as pd


def bulk_insert(file_name, table_name, dynamodb=None):
    if not dynamodb:
        # Already set up your credentials in AWSCLI
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)
    df = pd.read_csv(
        file_name, header=None, dtype=str
    )  # Add dtype=str to read all data as strings
    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = {
                # "id": str(index),  # Use the row index as the id
                "id": str(1),
                "date_val": str(row[0]),  # Access the date column by its index
            }
            # Add other columns here
            for i in range(1, 55):  # Assuming there are 53 data columns
                try:
                    # Try to convert to Decimal
                    item[f"data{i}"] = Decimal(str(row[i]))
                except InvalidOperation:
                    # If it fails, keep it as a string
                    item[f"data{i}"] = str(row[i])
            batch.put_item(Item=item)


if __name__ == "__main__":
    bulk_insert("./incert_files/data.csv", "TestTable1")
