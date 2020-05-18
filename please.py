import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import collections

app = dash.Dash()

df = dm.return_all_pd_data(token = API_TOKEN)

app.layout = html.Div(children=[
    html.H1(children='''
        Month for graph:
    '''),
    dcc.Dropdown(
        id = "input",
        options=[
            {'label': 'Jan', 'value': 1},
            {'label': 'Feb', 'value': 2},
            {'label': 'Mar', 'value': 3}
        ], value = 1
    ),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')])
def update_value(value):

    start = datetime.datetime(2018, value, 1, 0, 0, 0, 1)
    end = datetime.datetime(2018,  value + 1, 1, 0, 0, 0, 1)
    subset_df = df[ (df["lost_time"] > start) & (df["lost_time"] < end) ]

    x = pd.value_counts(subset_df.deal_source).index
    y = pd.value_counts(subset_df.deal_source).values

    return(dcc.Graph(
        id='output-graph',
        figure={
            'data': [
                {'x': x, 'y': y, 'type': 'bar', 'name': value},
            ],
            'layout': {
                'title': "You selected month: {}".format(value)
            }
        }
    ))


if __name__ == "__main__":

    app.run_server(debug = True)
