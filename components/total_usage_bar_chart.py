
import dash
from dash import Dash, html, dash_table, dcc, Output, Input
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px

#TODO: Add Error Checking to ensure months and years are valid (beginning not after end, etc.)
class TotalUsageBarChart:
    def __init__(self, app: Dash, df: pd.DataFrame, month_dict: dict):
        self.app = app
        self.df = df
        self.month_dict = month_dict
        self.layout = self.create_layout()
        self.register_callbacks(df)
        
    def create_layout(self):
        return html.Div([
            # Dropdown menu for selecting 'From' month
            dcc.Dropdown(
                id='from-month-dropdown',
                options=[
                    {'label': self.month_dict[month], 'value': month} for month in range(1, 13)
                ],
                value=self.df['Month'].min(),
                multi=False,
                style={'width': '50%'}
            ),

            # Dropdown menu for selecting 'To' month
            dcc.Dropdown(
                id='to-month-dropdown',
                options=[
                    {'label': self.month_dict[month], 'value': month} for month in range(1, 13)
                ],
                value=self.df['Month'].max(),
                multi=False,
                style={'width': '50%'}
            ),

            # Bar graph displaying the sum of 'Value' over the hour of the day
            dcc.Graph(id='hourly-bar-graph')
        ])


    def register_callbacks(self, df):
        @self.app.callback(
            Output('hourly-bar-graph', 'figure'),
            [Input('from-month-dropdown', 'value'),
            Input('to-month-dropdown', 'value')]
        )

        def update_graph(from_month, to_month):
            filtered_df = df[(df['Month'] >= from_month) & (df['Month'] <= to_month)]

            # Group by HourOfDay and sum the 'Value'
            hourly_sum_df = filtered_df.groupby('HourOfDay')['Value'].sum().reset_index()

            # Create a bar graph
            figure = {
                'data': [
                    {'x': hourly_sum_df['HourOfDay'], 'y': hourly_sum_df['Value'], 'type': 'bar', 'name': 'Hourly Sum'},
                ],
                'layout': {
                    'title': f'Sum of Value Over Hour of the Day ({self.month_dict[from_month]} to {self.month_dict[to_month]})',
                    'xaxis': {'title': 'Hour of the Day'},
                    'yaxis': {'title': 'Sum of Value'},
                }
            }
            return figure