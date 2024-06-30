import dash
from dash import html, dcc, callback, Input, Output, State
from components.total_usage_bar_chart import TotalUsageBarChart
import pandas as pd
import base64
import io

dash.register_page(__name__, path='/analytics', title='Analytics', name="Analytics Dashboard")

def layout():
    return html.Div([
        html.H1('The Analytics Page'),
        html.Div(id='chart-container'),
        dcc.Store(id='processed-data-store')  # Add this line
    ])

@callback(
    Output('processed-data-store', 'data'),
    Input('upload-data-store', 'data')
)

def process_data(stored_data):
    if stored_data is None or 'contents' not in stored_data:
        return None

    content_type, content_string = stored_data['contents'].split(',')
    decoded = base64.b64decode(content_string)
    try:
        if stored_data['filename'].endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif stored_data['filename'].endswith('.xlsx'):
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None
    except Exception as e:
        return None

    if df.empty:
        return None

    return df.to_dict('records')

@callback(
    Output('chart-container', 'children'),
    Input('processed-data-store', 'data')
)
def update_charts(processed_data):
    if processed_data is None:
        return html.Div("No data available. Please upload a file on the home page.")

    df = pd.DataFrame(processed_data)
    total_usage_bar_chart = TotalUsageBarChart(df)
    return total_usage_bar_chart.layout