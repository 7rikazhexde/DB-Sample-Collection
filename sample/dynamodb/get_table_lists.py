import os

import boto3


def list_tables(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    response = dynamodb.list_tables()
    return response["TableNames"]


if __name__ == "__main__":
    tables = list_tables()
    for table in tables:
        print(table)
    # print(os.environ['AWS_ACCESS_KEY_ID'])
    print(os.environ["LANG"])
