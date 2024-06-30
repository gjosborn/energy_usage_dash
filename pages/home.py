import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import base64
import datetime
import io

import pandas as pd

dash.register_page(
    __name__,
    path='/',
    title='Home',
    name='Home Page'
)

# Define the layout
def layout():
    return html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select File')
            ]),
            style={
                'width': '60%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '2px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'align-content': 'center',
            },
            multiple=False
        ),
        html.Button('Upload', id='upload-button', n_clicks=0),
        html.Div(id='output-data-upload'),
        # dcc.Store(id='upload-data-store', storage_type='session')
    ])

@callback(
    Output('output-data-upload', 'children'),
    Output('upload-data-store', 'data'),
    Input('upload-button', 'n_clicks'),
    State('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(n_clicks, contents, filename, last_modified):
    if n_clicks > 0 and contents is not None:
        children = parse_contents(contents, filename, last_modified)
        
        # Store the file data
        stored_data = {
            'contents': contents,
            'filename': filename,
            'last_modified': last_modified
        }
        
        return children, stored_data
    
    # If there are no contents or the button has not been clicked, return empty values
    return html.Div(), dash.no_update  # Use dash.no_update here

def parse_contents(contents, filename, last_modified):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an Excel file
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return html.Div([
                'Unsupported file format.'
            ])
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(last_modified)),

        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])
