from decimal import Decimal

import boto3
import pandas as pd


def bulk_insert(file_name, table_name, dynamodb=None):
    if not dynamodb:
        # Already set up your credentials in AWSCLI
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)
    df = pd.read_csv(file_name, header=None)  # Read data as is
    with table.batch_writer() as batch:
        for index, row in df.iterrows():
            item = {
                "id": str(index),  # Use the row index as the id
                "date_val": str(row[0]),  # Access the date column by its index
            }
            # Add other columns here
            for i in range(1, 55):  # Assuming there are 53 data columns
                try:
                    # Try to convert to Decimal
                    value = float(row[i])
                    if value.is_integer():
                        item[f"data{i}"] = Decimal(f"{value:.1f}")
                    else:
                        item[f"data{i}"] = Decimal(str(row[i]))
                except ValueError:
                    # Handle the ValueError, which occurs when the conversion fails
                    item[f"data{i}"] = str(row[i])
                except IndexError:
                    # Handle the IndexError, which occurs when the index is out of range
                    item[f"data{i}"] = None  # You can choose an appropriate action
                except Exception as e:
                    # Handle other exceptions, if any, by printing the error message
                    print(f"An error occurred: {str(e)}")
            batch.put_item(Item=item)


if __name__ == "__main__":
    bulk_insert("./incert_files/data.csv", "TestTable1")
