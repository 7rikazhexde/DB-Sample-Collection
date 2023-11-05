import json
import random
from datetime import datetime, timedelta

# 初期データ
skeletal_points = '[{"key_point": "2", "key_points": [{"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}]}, {"key_point": "3", "key_points": [{"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}, {"prob": "83.89", "x": "464", "y": "115"}]}]'
start_time = datetime(2023, 4, 1)
end_time = datetime(2023, 4, 5)
time_step = timedelta(minutes=30)

# 結果を格納するリスト
results = []

# 指定された時間範囲でループ
while start_time <= end_time:
    result = {
        "detected_date_time": start_time.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "date": start_time.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "detected_status": random.choice(["fallen", "normal"]),
        "id": random.choice(["camera1", "camera2"]),
        "skeletal_points": skeletal_points,
        "num_of_people": str(random.randint(0, 5)),
    }
    results.append(result)
    start_time += time_step

# JSONファイルに保存
with open("./incert_files/test_data.json", "w") as f:
    json.dump({"result": results}, f, indent=2)
