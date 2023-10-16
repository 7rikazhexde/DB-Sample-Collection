import csv
import time
from datetime import datetime

import pymysql
from tomlkit.toml_file import TOMLFile


def main():
    """data insertion process

    Note: Please refer to setup.md to create the table before execution.
    """
    # Obtaining database connection information
    toml = TOMLFile("./config.toml")
    toml_data = toml.read()
    toml_get_data = toml_data.get("database-mac")

    HOST = f'{toml_get_data["HOST"]}'
    PORT = int(toml_get_data["PORT"])
    USER = f'{toml_get_data["USER"]}'
    PASSWORD = f'{toml_get_data["PASSWORD"]}'
    DATABASE = f'{toml_get_data["DATABASE"]}'

    db_config = {
        "host": HOST,
        "port": PORT,
        "user": USER,
        "password": PASSWORD,
        "db": DATABASE,
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
    }

    # CSV file path
    csv_file = "data.csv"

    # Establish database connection
    connection = pymysql.connect(**db_config)

    try:
        with connection.cursor() as cursor:
            # Open CSV file
            with open(csv_file, "r") as csvfile:
                csv_reader = csv.reader(csvfile)

                # Create SQL query
                insert_query = """
                    INSERT INTO sample_tbl1 (date, action, ps_data1, ps_data2, ps_data3, ps_data4, ps_data5,
                                                ps_data6, ps_data7, ps_data8, ps_data9, ps_data10, ps_data11,
                                                ps_data12, ps_data13, ps_data14, ps_data15, ps_data16, ps_data17,
                                                ps_data18, ps_data19, ps_data20, ps_data21, ps_data22, ps_data23,
                                                ps_data24, ps_data25, ps_data26, ps_data27, ps_data28, ps_data29,
                                                ps_data30, ps_data31, ps_data32, ps_data33, ps_data34, ps_data35,
                                                ps_data36, ps_data37, ps_data38, ps_data39, ps_data40, ps_data41,
                                                ps_data42, ps_data43, ps_data44, ps_data45, ps_data46, ps_data47,
                                                ps_data48, ps_data49, ps_data50, ps_data51, ps_data52, ps_data53)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                data_to_insert = []
                for row in csv_reader:
                    # Convert date string to datetime object
                    date = datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S.%f")
                    # Combine data into tuples
                    data = (date,) + tuple(row[1:])
                    data_to_insert.append(data)

                # Insert data in bulk
                cursor.executemany(insert_query, data_to_insert)

            # Commit changes
            connection.commit()

    finally:
        # Close the connection
        connection.close()


if __name__ == "__main__":
    # Before data insertion
    start_time = time.perf_counter()
    print(f"Start:{str(start_time)}[sec]")
    # data insertion process
    main()
    # After data insertion
    end_time = time.perf_counter()
    print(f"End:{str(end_time)}[sec]")
    # Elapsed time measurement
    elasped_time = end_time - start_time
    print(f"elapsed_time: {elasped_time}[sec]\n")
