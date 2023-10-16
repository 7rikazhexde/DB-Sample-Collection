from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import pymysql
from dash import Dash, Input, Output, State, dcc, html
from tomlkit.toml_file import TOMLFile

# Obtaining database connection information
toml = TOMLFile("./config.toml")
toml_data = toml.read()
toml_get_data = toml_data.get("database-mac")

HOST = toml_get_data["HOST"]
PORT = int(toml_get_data["PORT"])
USER = toml_get_data["USER"]
PASSWORD = toml_get_data["PASSWORD"]
DATABASE = toml_get_data["DATABASE"]
TABLE = toml_get_data["TABLE"]

# Connect to SQL (MariaDB)
db = pymysql.connect(
    host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE
)

# Obtains the cursor
cursor = db.cursor()

# Execute SQL query to get minimum and maximum dates
cursor.execute(f"SELECT MIN(date), MAX(date) FROM {TABLE}")
min_date, max_date = cursor.fetchone()
# print(min_date)
# print(max_date)

# Create a Dash application
app = Dash(external_stylesheets=[dbc.themes.FLATLY])

# Defines the layout
app.layout = html.Div(
    [
        dcc.DatePickerRange(
            id="date-picker",
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            start_date=min_date,
            end_date=max_date,
        ),
        html.Button("Update Graph", id="update-button", n_clicks=0),
        html.Div(id="graph-container"),
    ]
)


# Define callbacks
@app.callback(
    Output("graph-container", "children"),
    Input("update-button", "n_clicks"),
    State("date-picker", "start_date"),
    State("date-picker", "end_date"),
)
def update_graph(n_clicks, start_date, end_date):
    # Fetches data only when the button is clicked.
    if n_clicks > 0:
        # Convert string to a datetime object (ignoring time information)
        start_date = datetime.strptime(start_date.split("T")[0], "%Y-%m-%d")
        end_date = datetime.strptime(end_date.split("T")[0], "%Y-%m-%d")

        # Obtain specified data by specifying a date range (DataFrame)
        end_date += timedelta(days=1)

        # Execute SQL query.
        cursor.execute(
            f"SELECT date, ps_data3, ps_data4 FROM {TABLE} WHERE date BETWEEN %s AND %s",
            (start_date, end_date),
        )

        # Fetch all the rows
        data = cursor.fetchall()

        # Split data into date and ps_data3, ps_data4
        dates = [row[0] for row in data]
        # print(type(dates))
        dates = pd.to_datetime([row[0] for row in data])
        # print(type(dates))
        ps_data3 = [row[1] for row in data]
        ps_data4 = [row[2] for row in data]

        # Create graphs
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=ps_data3, mode="lines", name="ps_data3"))
        fig.add_trace(go.Scatter(x=dates, y=ps_data4, mode="lines", name="ps_data4"))
        fig.update_layout(showlegend=True)

        # Returns dcc.Graph component
        return dcc.Graph(figure=fig)
    else:
        # If the button is not clicked, nothing is returned
        return None


# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
