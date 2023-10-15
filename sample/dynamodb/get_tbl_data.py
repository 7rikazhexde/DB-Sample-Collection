from decimal import Decimal

import boto3
import pandas as pd


def item_to_df(items, columns):
    data = []
    # 必要な列データのみを抽出して辞書型({key:val})の配列を作成する
    for item in items:
        extracted_data = {col: item[col] for col in columns}
        data.append(extracted_data)

    # リストをPandasのDataFrameに変換して日付でソート
    df = pd.DataFrame(data)
    df["date_val"] = pd.to_datetime(df["date_val"])
    df = df.sort_values("date_val").reset_index(drop=True)

    return df


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
    return items


def get_df_from_dynamodb(table_name, columns, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)

    # Scan the table with ProjectionExpression
    response = table.scan(ProjectionExpression=", ".join(columns))

    df = item_to_df(response["Items"], columns)

    return df


def get_items(date_from, date_to, table_name, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression="date_val between :date_from and :date_to",
        ExpressionAttributeValues={":date_from": date_from, ":date_to": date_to},
    )
    items = response["Items"]
    # 100は100.0とする
    for item in items:
        for key, value in item.items():
            if isinstance(value, Decimal):
                if value % 1 == 0:
                    item[key] = f"{value:.1f}"
                else:
                    item[key] = float(value)
    return items


def get_range_date_from_dynamodb(
    date_from, date_to, table_name, columns, dynamodb=None
):
    if not dynamodb:
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")

    table = dynamodb.Table(table_name)

    # Scan the table with FilterExpression and ProjectionExpression
    response = table.scan(
        FilterExpression="date_val between :date_from and :date_to",
        ProjectionExpression=", ".join(columns),
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

    df = item_to_df(response["Items"], columns)

    return df


if __name__ == "__main__":
    # 指定カラムのデータ取得
    df = get_df_from_dynamodb("TestTable1", ["date_val"])
    print(df)
    # 指定カラムのデータ取得(日付範囲指定)
    df = get_range_date_from_dynamodb(
        "2023-01-01", "2023-12-31", "TestTable1", ["date_val", "data5"]
    )
    print(df)
