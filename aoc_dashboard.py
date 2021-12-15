import base64
import json
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc
from aoc_scoreboard import AOCScoreboard
import plotly.express as px
from os.path import getmtime
import datetime
#from dash_bootstrap_templates import load_figure_template

try:
    import config
except ImportError:
    import default_config as config

my_template = 'plotly_white'

#alas having server issues with the bootstrap templates, disabling for now.
#load_figure_template(my_template)

from layout import layout

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.COSMO],
    prevent_initial_callbacks=True,
    suppress_callback_exceptions=True,
    url_base_pathname=config.base_url,
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
              Input('server-storage-interval', 'n_intervals'))
def update_output(data_uploaded, interval):
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
        server_status = dcc.Markdown(
            "Drag and drop or select a JSON file here to upload.")

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
    df = aoc.minutes_between_stars().round(2).reset_index()

    df.index.name = 'Name'
    print(df.index)
    print(df.to_dict(orient='records')[0])
    df.columns = [str(x) for x in df.columns]
    # time_between_stars = dbc.Table.from_dataframe(df,
    #                                               striped=True,
    #                                               bordered=True,
    #                                               hover=True)
    time_between_stars = dash.dash_table.DataTable(
        columns=[{
            "name": str(i),
            "id": str(i),
        } for i in df.columns],
        data=df.to_dict('records'),
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

    leaderboard_table_row = dbc.Row(
        [html.H3('Leaderboard Table By Day'), leaderboard_table])
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
