# DB-Sample-Collection

Repository for collecting and maintaining database-related examples and samples

## [MariaDB](./sample/mariadb/)

### Note

If you use the code, please create the configuration information([config.toml](./sample/mariadb/config.toml)) to connect to MariaDB.

### Write [data.csv](./sample/mariadb/data.csv) is written

[mariadb_incert.py](./sample/mariadb/mariadb_incert.py)

### Write [data.csv](./sample/mariadb/data.csv) is written(Bulk Insertion)

[mariadb_bulk_incert.py](./sample/mariadb/mariadb_bulk_incert.py)

### Example of data acquisition process and display by Dash

#### Example using [dcc.DatePickerRange](https://dash.plotly.com/dash-core-components/datepickerrange)

##### Data received in SQL query (list)

[dash_mariadb_range_dt_pick_multi_btn.py](./sample/mariadb/dash_mariadb_range_dt_pick_multi_btn.py)

##### Convert data (list) received by SQL query into a DataFrame

[dash_mariadb_range_dtt_dt_pick_multi_btn.py](./sample/mariadb/dash_mariadb_range_dtt_dt_pick_multi_btn.py)

## [MongoDB](./sample/mongodb/)

Will be described in the future.

## [DynamoDB](./sample/dynamodb/)

### Example of API Gateway, Lambda function, and DynamoDB configuration

### Note

This repository deals only with code. Please check the following article for configuration (*Japanese article)

<https://7rikazhexde-techlog.hatenablog.com/>

### Create [sample json data](./sample/dynamodb/incert_files/test_data.json)

[create_json_file.py](./sample/dynamodb/create_json_file.py)

### Call `put_item` [sample json data](./sample/dynamodb/incert_files/test_data.json)

[incert_data_json.py](./sample/dynamodb/incert_data_json.py)

### Sending GET requests (via API Gateway)

[request_api.py](./sample/dynamodb/request_api.py)
