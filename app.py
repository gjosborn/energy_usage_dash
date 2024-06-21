import dash
from dash import Dash, html, dash_table, dcc, Output, Input
from dash_bootstrap_components.themes import BOOTSTRAP
import pandas as pd
import plotly.express as px

df = pd.read_csv('energy_usage.csv')

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

app = Dash(external_stylesheets=[BOOTSTRAP], use_pages=True, title='Energy Usage Dashboard')
    
app.layout = html.Div([
    # Dropdown menu for selecting 'From' month
    dcc.Dropdown(
        id='from-month-dropdown',
        options=[
            {'label': month_dict[month], 'value': month} for month in range(1, 13)
        ],
        value=df['Month'].min(),
        multi=False,
        style={'width': '50%'}
    ),

    # Dropdown menu for selecting 'To' month
    dcc.Dropdown(
        id='to-month-dropdown',
        options=[
            {'label': month_dict[month], 'value': month} for month in range(1, 13)
        ],
        value=df['Month'].max(),
        multi=False,
        style={'width': '50%'}
    ),

    # Bar graph displaying the sum of 'Value' over the hour of the day
    dcc.Graph(id='hourly-bar-graph'),
    dash.page_container
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
            'title': f'Sum of Value Over Hour of the Day ({month_dict[from_month]} to {month_dict[to_month]})',
            'xaxis': {'title': 'Hour of the Day'},
            'yaxis': {'title': 'Sum of Value'},
        }
    }
    return figure
    

if __name__ == '__main__':
    app.run(debug=True)