import dash
from dash import Dash, html, dash_table, dcc, Output, Input
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px
from components.navbar import create_navbar

month_dict = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

df = pd.read_csv('energy_usage.csv')
app = Dash(__name__, external_stylesheets=[BOOTSTRAP], use_pages=True, title='Energy Usage Dashboard')

from pages import analytics
analytics.page_load(app, df, month_dict)


app.layout = html.Div([
    create_navbar(),
    dash.page_container
])


if __name__ == '__main__':
    app.run(debug=True)