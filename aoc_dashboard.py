import base64
import json
import io
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from hashlib import sha256
from aoc_scoreboard import AOCScoreboard
import plotly.express as px
from dash_bootstrap_templates import load_figure_template

my_template = 'cosmo'

load_figure_template(my_template)

from layout import layout

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.COSMO],
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True,
    url_base_pathname='/aoc/',  #change this to a config
    title='AOC Dashboard',
    meta_tags=[{
        'name': 'description',
        'content': 'AOC Leaderboard JSON to HTML Dashboard'
    }, {
        'name':
        'keywords',
        'content':
        'advent of code, json, dashboard, leaderboard, aoc, aoc2019, aoc2020'
    }, {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1"
    }],
)

server = app.server

app.layout = html.Div(layout)


@app.callback(
    Output('leaderboard-data', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
)
def update_output(content, name):
    if content:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)
        return json.loads(decoded.decode('utf-8'))
    else:
        return dash.no_update


@app.callback(
    [
        Output('line-graph-div', 'children'),
        Output('daily-leaderboard-div', 'children'),
    ],
    Input('leaderboard-data', 'data'),
)
def update_output(data):
    if data:
        aoc = AOCScoreboard(json_dict=data)
        heatmap = px.imshow(
            aoc.make_daily_leaderboard(show_possibles=False).drop(
                columns=['Total']).fillna(0),
            labels={'color': 'Points'},
            template=my_template,
        )

        leaderboard_table = dbc.Table.from_dataframe(
            aoc.make_daily_leaderboard().reset_index(),
            striped=True,
            bordered=True,
            hover=True,
        )

        leaderboard_table_row = dbc.Row(
            [html.H3('Leaderboard Table By Day'), leaderboard_table])
        leaderboard_heatmap_row = dbc.Row([
            html.H3('Points by Day Heatmap'),
            dcc.Graph(figure=heatmap),
        ])

        return [
            dcc.Graph(figure=aoc.line_graph()),
            dbc.Col([leaderboard_table_row, leaderboard_heatmap_row],
                    style={'padding': '20px'})
        ]
    else:
        return dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True)
