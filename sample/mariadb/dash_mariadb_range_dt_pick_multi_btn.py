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

# Connect to SQL (MariaDB)
db = pymysql.connect(
    host=HOST, port=PORT, user=USER, password=PASSWORD, database=DATABASE
)

# Obtains the cursor
cursor = db.cursor()

# Execute SQL query to get minimum and maximum dates
cursor.execute("SELECT MIN(date), MAX(date) FROM ec_sol_pes_tbl")
min_date, max_date = cursor.fetchone()

# Create a Dash application
app = Dash(__name__)

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
        dcc.Graph(id="graph"),
    ]
)


# Define callbacks
@app.callback(
    Output("graph", "figure"),
    Input("update-button", "n_clicks"),
    State("date-picker", "start_date"),
    State("date-picker", "end_date"),
)
def update_graph(n_clicks, start_date, end_date):
    # Execute SQL query
    cursor.execute(
        "SELECT date, ps_data3, ps_data4 FROM ec_sol_pes_tbl WHERE date BETWEEN %s AND %s",
        (start_date, end_date),
    )

    # Fetch all the rows
    data = cursor.fetchall()

    # Split data into date and ps_data3, ps_data4
    dates = [row[0] for row in data]
    ps_data3 = [row[1] for row in data]
    ps_data4 = [row[2] for row in data]

    # Create graphs
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=ps_data3, mode="lines", name="ps_data3"))
    fig.add_trace(go.Scatter(x=dates, y=ps_data4, mode="lines", name="ps_data4"))
    fig.update_layout(showlegend=True)

    return fig


# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
