from decimal import Decimal

import boto3


def get_items(date_from, date_to, table_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression="date_val between :date_from and :date_to",
        ExpressionAttributeValues={":date_from": date_from, ":date_to": date_to},
    )
    items = response["Items"]
    for item in items:
        for key, value in item.items():
            if isinstance(value, Decimal):
                if value % 1 == 0:
                    item[key] = f"{value:.1f}"
                else:
                    item[key] = float(value)
    return items


if __name__ == "__main__":
    items = get_items("2023-03-03", "2023-03-06", "TestTable1")
    for item in items:
        print(item)
