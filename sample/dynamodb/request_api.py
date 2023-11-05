from typing import Optional

import boto3
import pandas as pd
import requests
from requests_aws4auth import AWS4Auth

# AWS認証情報を直接指定
session = boto3.Session()
credentials = session.get_credentials()
aws_access_key_id = credentials.access_key
aws_secret_access_key = credentials.secret_key
region_name = session.region_name
# 「API > ステージ > URLを呼び出す 」より参照
api_endpoint = "ステージ込みのエンドポイントを指定する"

# AWS4Authオブジェクトを作成
auth = AWS4Auth(aws_access_key_id, aws_secret_access_key, region_name, "execute-api")


def get_req(
    id: str,
    columns: list,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
):
    # リクエストを作成
    url = f"{api_endpoint}?id={id}"
    if start_date is not None:
        url += f"&start_date={start_date}"
    if end_date is not None:
        url += f"&end_date={end_date}"
    response = requests.get(url, auth=auth)

    # レスポンスを表示
    data = response.json()

    new_data = [[item[column] for column in columns] for item in data["result"]]

    # new_dataは上記で作成したリスト
    df = pd.DataFrame(new_data, columns=columns)
    return df


if __name__ == "__main__":
    columns = ["id", "date_val", "detected_status", "num_of_people", "skeletal_points"]
    df = get_req("camera1", columns, "2023-04-01", "2023-04-02")
    print(df)
    # get_req("camera1", columns)
