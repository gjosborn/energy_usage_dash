import dash
from components.navbar import create_navbar
from components.total_usage_bar_chart import TotalUsageBarChart
from dash import html, dcc, callback, Input, Output

def layout():
    return html.Div([
        html.H1('404 Page Not Found'),
    ])