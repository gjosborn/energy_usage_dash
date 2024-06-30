from dash import html, dcc, Output, Input, clientside_callback, ClientsideFunction
import pandas as pd
import json

class TotalUsageBarChart:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.month_dict = {
            1: 'January', 2: 'February', 3: 'March', 4: 'April',
            5: 'May', 6: 'June', 7: 'July', 8: 'August',
            9: 'September', 10: 'October', 11: 'November', 12: 'December'
        }
        self.layout = self.create_layout()

    def create_layout(self):
        return html.Div([
            dcc.Store(id='chart-data-store', data=self.df.to_dict('records')),
            dcc.Dropdown(
                id='from-month-dropdown',
                options=[
                    {'label': self.month_dict[month], 'value': month} for month in range(1, 13)
                ],
                value=self.df['Month'].min() if 'Month' in self.df.columns and not self.df.empty else 1,
                multi=False,
                style={'width': '50%'}
            ),
            dcc.Dropdown(
                id='to-month-dropdown',
                options=[
                    {'label': self.month_dict[month], 'value': month} for month in range(1, 13)
                ],
                value=self.df['Month'].max() if 'Month' in self.df.columns and not self.df.empty else 12,
                multi=False,
                style={'width': '50%'}
            ),
            dcc.Graph(id='hourly-bar-graph'),
            html.Div(id='chart-debug-output')  # Add this for debugging
        ])

    def register_callbacks(self, app):
        clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_graph'
            ),
            Output('hourly-bar-graph', 'figure'),
            [Input('from-month-dropdown', 'value'),
             Input('to-month-dropdown', 'value'),
             Input('chart-data-store', 'data')]
        )

        @app.callback(
            Output('chart-debug-output', 'children'),
            [Input('chart-data-store', 'data')]
        )
        def debug_data(data):
            return f"Data in store: {len(data)} rows. First row: {json.dumps(data[0] if data else {})}"