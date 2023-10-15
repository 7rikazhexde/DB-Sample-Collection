import boto3


def create_table(dynamodb=None):
    if not dynamodb:
        # For DynamoDB-Local

        # Not set up your credentials in AWSCLI
        # dynamodb = boto3.resource('dynamodb',
        #                          region_name='us-west-2',
        #                          endpoint_url="http://localhost:8000",
        #                          aws_access_key_id='[id]', #For local version, any id
        #                          aws_secret_access_key='[pw]')

        # Already set up your credentials in AWSCLI
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName="TestTable1",
        KeySchema=[
            {"AttributeName": "id", "KeyType": "HASH"},  # Partition key
            {"AttributeName": "date_val", "KeyType": "RANGE"},  # Sort key
        ],
        AttributeDefinitions=[
            {"AttributeName": "id", "AttributeType": "S"},
            {"AttributeName": "date_val", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    return table


if __name__ == "__main__":
    table = create_table()
    print("Table status:", table.table_status)
