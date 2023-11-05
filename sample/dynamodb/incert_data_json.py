import json

import boto3

# DynamoDBオブジェクトを取得
# For DynamoDB-Local
# dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="https://dynamodb.ap-northeast-1.amazonaws.com",  # DynamoDBのエンドポイントURL
)

# テーブル名を定義
table_name = "TestJsonTable1"

# テーブルオブジェクトを取得
table = dynamodb.Table(table_name)

file_name = "./incert_files/test_data.json"

# JSONファイルからデータを読み込む
with open(file_name, "r") as f:
    data = json.load(f)

# データをテーブルに書き込む
for item in data["result"]:
    table.put_item(Item=item)

print("Data written to table successfully.")
