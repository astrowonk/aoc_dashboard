import base64
import json
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dash_table import FormatTemplate
from dash.dash_table.Format import Format, Scheme
from aoc_scoreboard import AOCScoreboard
import plotly.express as px
from os.path import getmtime
import datetime
import dash_dataframe_table
import numpy as np
#from dash_bootstrap_templates import load_figure_template

try:
    import config
except ImportError:
    import default_config as config

from pathlib import Path

parent_dir = Path().absolute().stem

my_template = 'plotly_white'

#alas having server issues with the bootstrap templates, disabling for now.
#load_figure_template(my_template)

from layout import layout

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.COSMO],
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True,
    url_base_pathname=config.base_url or f"/dash/{parent_dir}/",
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


@app.callback([
    Output('line-graph-div', 'children'),
    Output('daily-leaderboard-div', 'children'),
    Output('server-status', 'children'),
    Output('time-between-stars-div', 'children')
], Input('leaderboard-data', 'data'),
              Input('server-storage-interval', 'n_intervals'),
              Input('time-between-stars-option', 'value'))
def update_output(data_uploaded, interval, stars_option):
    file_mod_time = None
    ctx = dash.callback_context
    an_id = ctx.triggered[0]['prop_id'].split('.')[0]
    ## should not refresh to check local storage if in upload mode
    if config.server_mode == 'upload' and an_id == 'server-storage-interval':
        return dash.no_update, dash.no_update
    if config.server_mode == 'upload' and data_uploaded:
        data = data_uploaded
    elif config.server_mode == 'local':
        data = json.loads(open(config.json_file).read())
        file_mod_time = datetime.datetime.fromtimestamp(
            getmtime(config.json_file))
    else:
        return dash.no_update

    if file_mod_time:
        mytimestring = file_mod_time.strftime('%Y-%m-%d %H:%M:%S')
        server_status = dcc.Markdown(
            f"Server-side JSON last updated: {mytimestring}")
    elif config.server_mode == 'upload':
        server_status = None

    aoc = AOCScoreboard(json_dict=data)
    heatmap = px.imshow(
        aoc.make_daily_leaderboard(show_possibles=False).drop(
            columns=['Total']).fillna(0),
        labels={'color': 'Points'},
        template=my_template,
    )
    tooltip_map = {
        'high':
        "Score if player was the next to solve each star, achieving the high possible remaining points for each day.",
        'low':
        "Score if player was the last to solve each star, achieving the low possible remaining points for each day (2).",
    }

    def format_header(x):
        if str(x).isnumeric():
            return html.A(
                str(x),
                href=f"https://adventofcode.com/{data['event']}/day/{x}")
        else:
            return html.Span(x, id=f"{x.lower().replace(' ','-')}-header")

    leaderboard_df = aoc.make_daily_leaderboard().reset_index()
    leaderboard_df.columns = [str(x) for x in leaderboard_df.columns]
    print(leaderboard_df.columns)
    leaderboard_table = dbc.Table.from_enhanced_dataframe(
        aoc.make_daily_leaderboard().reset_index(),
        striped=True,
        bordered=True,
        hover=True,
        header_callable=format_header,
        float_format='.0f')
    df_stars = aoc.minutes_between_stars().round(2).reset_index()

    df_stars.index.name = 'Name'

    df_stars.columns = [str(x) for x in df_stars.columns]
    format = Format(precision=2, scheme=Scheme.fixed)
    if stars_option == 'Rank':
        format = Format()
        cols = [x for x in df_stars.columns if x != 'Name']
        df_stars.replace(0, np.NaN, inplace=True)

        for col in cols:
            df_stars[col] = df_stars[col].rank()
        df_stars['Average Rank'] = df_stars[cols].mean(axis=1).round(2)
    time_between_stars = dash.dash_table.DataTable(
        columns=[{
            "name": str(i),
            "id": str(i),
            'format': format,
            'type': 'numeric'
        } for i in df_stars.columns],
        data=df_stars.to_dict('records'),
        sort_action="native",
        sort_mode="single",
        style_cell={
            'fontSize': 16,
            'font-family': 'Source Sans Pro'
        },
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[{
            'if': {
                'row_index': 'odd'
            },
            'backgroundColor': 'rgba(0, 0, 0, 0.05)',
        }],
    )

    leaderboard_table_row = dbc.Row([
        html.H3('Leaderboard Table By Day'), leaderboard_table,
        html.Div([
            dbc.Tooltip(tooltip_map['high'],
                        target='highest-possible-total-header',
                        placement='top'),
            dbc.Tooltip(tooltip_map['low'],
                        target='lowest-possible-total-header',
                        placement='top')
        ])
    ])
    leaderboard_heatmap_row = dbc.Row([
        html.H3('Points by Day Heatmap'),
        dcc.Graph(figure=heatmap),
    ])

    return [
        dcc.Graph(figure=aoc.line_graph()),
        dbc.Col([leaderboard_table_row, leaderboard_heatmap_row],
                style={'padding': '20px'}), server_status, time_between_stars
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
