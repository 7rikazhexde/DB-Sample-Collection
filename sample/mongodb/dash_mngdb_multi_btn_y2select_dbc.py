from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html
from pymongo import MongoClient
from tomlkit.toml_file import TOMLFile

# Obtaining database connection information
toml = TOMLFile("./config.toml")
toml_data = toml.read()
toml_get_data = toml_data.get("database-mac")

HOST = toml_get_data["HOST"]
PORT = str(toml_get_data["PORT"])
USER = toml_get_data["USER"]
PASSWORD = toml_get_data["PASSWORD"]
DATABASE = toml_get_data["DATABASE"]
COLLECTION = toml_get_data["COLLECTION"]

# Connect to MongoDB
client = MongoClient(f"mongodb://{USER}:{PASSWORD}@{HOST}:{PORT}/")
# Select DB
db = client[f"{DATABASE}"]
# Select a collection
collection = db[f"{COLLECTION}"]
# Get data
min_date = collection.find().sort("col1", 1).limit(1)[0]["col1"]
max_date = collection.find().sort("col1", -1).limit(1)[0]["col1"]

# Create a Dash application
app = Dash(external_stylesheets=[dbc.themes.FLATLY])

# Defines the layout
app.layout = html.Div(
    [
        dbc.Row(
            style={"margin-top": "10px"},
            children=[
                dbc.Col(
                    dcc.DatePickerRange(
                        id="date-picker",
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        start_date=min_date,
                        end_date=max_date,
                    ),
                    width=3,
                    style={"margin-top": "2px", "margin-left": "5px"},
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="yaxis-column1",
                        options=[
                            {"label": i, "value": i}
                            for i in ["col" + str(j) for j in range(4, 56)]
                        ],
                        value="col4",
                    ),
                    width=1,
                    style={"margin-top": "5px"},
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="yaxis-column2",
                        options=[
                            {"label": i, "value": i}
                            for i in ["col" + str(j) for j in range(4, 56)]
                        ],
                        value="col5",
                    ),
                    width=1,
                    style={"margin-top": "5px"},
                ),
                dbc.Col(
                    dbc.Button("Update Graph", id="update-button", n_clicks=0),
                    width=2,
                    style={"margin-top": "5px"},
                ),
            ],
        ),
        html.Div(id="graph-container"),
    ]
)


# Define callbacks
@app.callback(
    Output("graph-container", "children"),
    Input("update-button", "n_clicks"),
    State("date-picker", "start_date"),
    State("date-picker", "end_date"),
    State("yaxis-column1", "value"),
    State("yaxis-column2", "value"),
)
def update_graph(
    n_clicks, start_date, end_date, yaxis_column_name1, yaxis_column_name2
):
    # Fetches data only when the button is clicked.
    if n_clicks > 0:
        # Convert string to a datetime object (ignoring time information)
        start_date = datetime.strptime(start_date.split("T")[0], "%Y-%m-%d")
        end_date = datetime.strptime(end_date.split("T")[0], "%Y-%m-%d")

        # In end_date, add one day to include data recorded in YYYYY-MM-DD
        end_date += timedelta(days=1)

        # Get data in the range of start_date and end_date.
        data = list(collection.find({"col1": {"$gte": start_date, "$lte": end_date}}))
        col1_dates = [row["col1"].date() for row in data]
        yaxis_data1 = [row[yaxis_column_name1] for row in data]
        yaxis_data2 = [row[yaxis_column_name2] for row in data]

        # Create graphs
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=col1_dates, y=yaxis_data1, mode="lines", name=yaxis_column_name1
            )
        )
        fig.add_trace(
            go.Scatter(
                x=col1_dates, y=yaxis_data2, mode="lines", name=yaxis_column_name2
            )
        )
        fig.update_layout(showlegend=True)

        # Returns dcc.Graph component.
        return dcc.Graph(figure=fig)
    else:
        # If the button is not clicked, nothing is returned
        return None


# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
