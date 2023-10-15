import boto3
import pandas as pd


def bulk_insert(file_name, table_name, dynamodb=None):
    if not dynamodb:
        # Already set up your credentials in AWSCLI
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)
    df = pd.read_csv(
        file_name, header=None
    )  # Add header=None to read csv without headers
    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = {
                "id": str(index),  # Use the row index as the id
                "date_val": str(row[0]),  # Access the date column by its index
                # Add other columns here
            }
            if (
                item["id"] and item["date_val"]
            ):  # Ensure both id and date_val are not empty
                batch.put_item(Item=item)


if __name__ == "__main__":
    bulk_insert("data.csv", "TestTable1")
