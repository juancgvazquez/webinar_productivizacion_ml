import base64
import datetime
import io
import plotly.graph_objs as go
import cufflinks as cf
import requests
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import json
import pandas as pd
import plotly.tools as tls

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
requests
colors = {
"graphBackground": "#F5F5F5",
"background": "#ffffff",
"text": "#000000"
}

app.layout = html.Div([
    html.Div(id='service-status'),
    dcc.Interval(id='interval1', interval=5 * 1000, n_intervals=0),
    dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    # Allow multiple files to be uploaded
    multiple=True
),
dcc.Graph(id='Mygraph'),
html.Div(id='output-data-upload')
])


@app.callback(dash.dependencies.Output('service-status', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    try: 
        response = requests.get('http://localhost:8000/api/health/heartbeat').json()
        if response['is_alive'] == True:
            return html.H3('Service Status: Alive',style={"color":"green"})
    except requests.exceptions.RequestException:
        return html.H3('Service Status: Dead',style={"color":"red"})

@app.callback(Output('Mygraph', 'figure'), [
Input('upload-data', 'contents'),
Input('upload-data', 'filename')
])
def update_graph(contents, filename):
    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        #df = df.set_index(df.columns[0])
        df=df.iloc[:,:5]
        fig = tls.make_subplots(rows=3, cols=2,vertical_spacing=0.25,horizontal_spacing=0.25)
        counterrow = 0
        countercol = 1
        for col in df.columns:
            if counterrow == 3:
                counterrow=1
                countercol+=1
            else:
                counterrow +=1
            trace = go.Histogram(x=df[col], nbinsx=100,name=col)
            fig.append_trace(trace,counterrow,countercol)
        return fig
    else:
        fig = tls.make_subplots(rows=8, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009) 
        return fig

def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


@app.callback(Output('output-data-upload', 'children'),
          [
Input('upload-data', 'contents'),
Input('upload-data', 'filename')
])
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        payload = df.to_dict(orient='records')
        listaresponse=[]
        for x in range(len(payload)):
            response = requests.post('http://localhost:8000/api/model/predict',data=json.dumps(payload[x]),headers={'token':'6a7c24d3-6d1f-4129-87be-d7aeba15729e'}).json()
            listaresponse.append(response)
            print(x,'°°°°',response)
        df = pd.DataFrame(listaresponse).reset_index()
        #print(df)
        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
        ])

    return table


if __name__ == '__main__':
    app.run_server(debug=True)