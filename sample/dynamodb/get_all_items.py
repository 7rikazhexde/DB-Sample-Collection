from decimal import Decimal

import boto3


def get_all_items(table_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response["Items"]
    for item in items:
        for key, value in item.items():
            if isinstance(value, Decimal):
                if value % 1 == 0:
                    item[key] = f"{value:.1f}"
                else:
                    item[key] = float(value)
    # return response['Items']
    return items


if __name__ == "__main__":
    items = get_all_items("TestTable1")
    for item in items:
        print(item)
