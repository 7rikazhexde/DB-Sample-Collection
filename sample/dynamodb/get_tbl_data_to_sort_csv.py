from decimal import Decimal

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
    items = response["Items"]
    for item in items:
        for key, value in item.items():
            if isinstance(value, Decimal):
                if value % 1 == 0:
                    item[key] = f"{value:.1f}"
                else:
                    item[key] = float(value)
    return items


def save_to_csv(items, file_name):
    df = pd.DataFrame(items)
    # Reorder the columns in the desired order
    df = df[["date_val"] + [f"data{i}" for i in range(1, 55)]]
    # Sort the DataFrame by date_val in ascending order
    df = df.sort_values("date_val")
    df.to_csv(file_name, index=False, header=False)


def sort_df_items(items):
    df = pd.DataFrame(items)
    # Reorder the columns in the desired order
    df = df[["date_val"] + [f"data{i}" for i in range(1, 55)]]
    # Sort the DataFrame by date_val in ascending order
    df = df.sort_values("date_val").reset_index(drop=True)

    ## date_val列をdatetime型に変換
    # df['date_val'] = pd.to_datetime(df['date_val'])
    #
    ## data1列をstr型に変換
    # df['data1'] = df['data1'].astype(str)
    #
    ## data2からdata54までの列をfloat型に変換
    # for i in range(2, 55):
    #    df['data'+str(i)] = df['data'+str(i)].astype(float)

    ## date_val列をdatetime型に変換
    # df['date_val'] = pd.to_datetime(df['date_val'])
    ## 条件に合う行を抽出
    # df_filtered = df[(df['date_val'] > '2023-03-03') & (df['date_val'] < '2023-03-06')]
    ## 必要な列だけを抽出
    # df = df_filtered[['date_val', 'data5', 'data6']]

    return df


if __name__ == "__main__":
    items = get_items("2023-03-03", "2023-03-06", "TestTable1")
    # print(items)
    df = sort_df_items(items)
    # print(df)
    # save_to_csv(items, 'get_tbl_data.csv')
