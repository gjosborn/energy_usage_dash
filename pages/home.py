import dash
from dash import html, dcc, callback, Input, Output
from components.navbar import create_navbar

dash.register_page(
    __name__,
    path='/',
    title='Home'
)


layout = html.Div([
    html.H1('The Home Page'),
    html.P('Welcome to the Home page!')
])
