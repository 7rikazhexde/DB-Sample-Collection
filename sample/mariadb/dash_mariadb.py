import plotly.graph_objects as go
import pymysql
from dash import Dash, dcc, html
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

# Execute SQL query
cursor.execute("SELECT date, ps_data3, ps_data4 FROM ec_sol_pes_tbl")

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
# Show legend (may be omitted if more than one legend is specified)
fig.update_layout(showlegend=True)

# Create a Dash application
app = Dash(__name__)

# Defines the layout
app.layout = html.Div([dcc.Graph(figure=fig)])

# Run the application
if __name__ == "__main__":
    app.run_server(debug=True)
