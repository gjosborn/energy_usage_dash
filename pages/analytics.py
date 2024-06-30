import dash
from components.navbar import create_navbar
from components.total_usage_bar_chart import TotalUsageBarChart
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__, 
    path='/analytics', 
    title='Analytics',
    name="Analytics Dashboard"
)

def page_load(app, df, month_dict):
    global total_usage_bar_chart
    total_usage_bar_chart = TotalUsageBarChart(app=app, df=df, month_dict=month_dict)

def layout():
    return html.Div([
        html.H1('The Analytics Page'),
        total_usage_bar_chart.layout
    ])
    
