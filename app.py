from dash import Dash, html, dash_table, dcc, Output, Input
import pandas as pd
import plotly.express as px

df = pd.read_csv('energy_usage.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Hourly Sum of Values"),

    # Dropdown menu for selecting 'From' month
    dcc.Dropdown(
        id='from-month-dropdown',
        options=[
            {'label': 'January', 'value': 1},
            {'label': 'February', 'value': 2},
            {'label': 'March', 'value': 3},
            {'label': 'April', 'value': 4},
            {'label': 'May', 'value': 5},
            {'label': 'June', 'value': 6},
            {'label': 'July', 'value': 7},
            {'label': 'August', 'value': 8},
            {'label': 'September', 'value': 9},
            {'label': 'October', 'value': 10},
            {'label': 'November', 'value': 11},
            {'label': 'December', 'value': 12},
        ],
        value=df['Month'].min(),
        multi=False,
        style={'width': '50%'}
    ),

    # Dropdown menu for selecting 'To' month
    dcc.Dropdown(
        id='to-month-dropdown',
        options=[
            {'label': month, 'value': month} for month in df['Month'].unique()
        ],
        value=df['Month'].max(),
        multi=False,
        style={'width': '50%'}
    ),

    # Bar graph displaying the sum of 'Value' over the hour of the day
    dcc.Graph(id='hourly-bar-graph'),
])


# Define callback to update the graph based on dropdown selections
@app.callback(
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
            'title': f'Sum of Value Over Hour of the Day ({from_month} to {to_month})',
            'xaxis': {'title': 'Hour of the Day'},
            'yaxis': {'title': 'Sum of Value'},
        }
    }
    return figure


if __name__ == '__main__':
    app.run(debug=True)