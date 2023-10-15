from datetime import datetime, timedelta

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, dcc, html
from get_tbl_data import get_df_from_dynamodb, get_range_date_from_dynamodb
from tomlkit.toml_file import TOMLFile

# Obtaining database connection information
toml = TOMLFile("./config.toml")
toml_data = toml.read()
toml_get_data = toml_data.get("database-mac")

TABLE = toml_get_data["TABLE"]

# Get only date data from DynamoDB and find min/max values
df = get_df_from_dynamodb(TABLE, ["date_val"])
min_date = df["date_val"].min()
max_date = df["date_val"].max()

# List of target data (column names) to be retrieved from DynamoDB
get_data_list = ["date_val", "data5", "data6"]

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

        # In end_date, add one day to include data recorded in YYYYY-MM-DD
        end_date += timedelta(days=1)

        # Convert the date to a string in ISO format (ISO 8601) since it is treated as a string in FilterExpression in DynamoDB
        start_date = start_date.isoformat()
        end_date = end_date.isoformat()

        # Obtain specified data by specifying a date range (DataFrame)
        df = get_range_date_from_dynamodb(start_date, end_date, TABLE, get_data_list)
        # Define data
        df[get_data_list[0]] = df[get_data_list[0]].astype(str)
        df[get_data_list[1]] = df[get_data_list[1]].astype(float)
        df[get_data_list[2]] = df[get_data_list[2]].astype(float)

        # Create graphs
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=df["date_val"], y=df["data6"], mode="lines", name="data6")
        )
        fig.update_layout(showlegend=True)

        # Returns dcc.Graph component
        return dcc.Graph(figure=fig)
    else:
        # If the button is not clicked, nothing is returned
        return None


# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
