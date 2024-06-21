import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    path='/forecasting',
    title='Forecasting'
)

layout = html.Div([
    html.H1('Forecasting Page'),
    html.P('Welcome to the forecasting page!')
])
