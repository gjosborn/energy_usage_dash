import dash
from dash import html, dcc, callback, Input, Output

dash.register_page(
    __name__,
    path='/analytics',
    title='Analytics'
)

layout = html.Div([
    html.H1('The Analytics Page'),
    html.P('Welcome to the Analytics page!')
])
