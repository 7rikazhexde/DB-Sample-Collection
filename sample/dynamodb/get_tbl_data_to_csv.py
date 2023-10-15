import boto3
import pandas as pd


def get_items(date_from, date_to, table_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression="date_val between :date_from and :date_to",
        ExpressionAttributeValues={":date_from": date_from, ":date_to": date_to},
    )
    return response["Items"]


def save_to_csv(items, file_name):
    df = pd.DataFrame(items)
    df.to_csv(file_name, index=False)


if __name__ == "__main__":
    items = get_items("2023-03-03", "2023-03-31", "TestTable1")
    save_to_csv(items, "get_tbl_data.csv")
