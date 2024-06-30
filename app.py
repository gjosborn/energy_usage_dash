import dash
from dash import Dash, html, dash_table, dcc, Output, Input
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px
from components.navbar import create_navbar
from components.total_usage_bar_chart import TotalUsageBarChart

df = pd.read_csv('energy_usage.csv')
app = Dash(__name__, external_stylesheets=[BOOTSTRAP], use_pages=True, title='Energy Usage Dashboard')
TotalUsageBarChart(pd.DataFrame()).register_callbacks(app)

app.layout = html.Div([
    create_navbar(),
    dcc.Store(id='upload-data-store', storage_type='session'),
    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True)