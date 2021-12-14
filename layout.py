from dash import html, dcc
import dash_bootstrap_components as dbc

markdown_style = {
    "width": "100%",
    'margin': '10px',
}

intro_text = """

This dashboard is powered by the [AOC Scoreboard class](https://github.com/astrowonk/aoc_scoreboard) which processes and converts
the json from the Advent of Code private dashboard API.

The uploaded data is stored in a [dash core component Store](https://dash.plotly.com/dash-core-components/store) using local storage. 
The json data is only stored on your own browser and is never saved on the server.

"""

main_text = """
### Advent of Code Private Leaderboard Dashboard


"""
main_interface = html.Div([
    dcc.Markdown(main_text, style=markdown_style),
    html.Div([
        html.Div([
            dcc.Upload(
                id='upload-data',
                children=[
                    'Drag and Drop or ',
                    html.A('Select a .json file from a private leaderboard')
                ],
                style={
                    #     'width': '100%',
                    'height': '80px',
                    #     'lineHeight': '70px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '15px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                #  Allow multiple files to be uploaded
                multiple=False,
                max_size=
                1.5E6  #1.5MB I think, this is based on the practical limits of dcc.Store, files should be well under this
            )
        ])
    ]),
])

about_tab_content = html.Div(dcc.Markdown(
    intro_text,
    style=markdown_style,
))

line_graph_tab_content = html.Div(id='line-graph-div')
daily_leadboard_content = html.Div(id='daily-leaderboard-div')
time_between_stars = html.Div(id='time-between-stars-div')

tabs = dbc.Tabs([
    dbc.Tab(line_graph_tab_content, label='Line Graph'),
    dbc.Tab(daily_leadboard_content, label='Daily Leaderboard'),
    dbc.Tab(about_tab_content, label="About"),
])

layout = dbc.Container([
    dcc.Store(id='leaderboard-data', storage_type='local'),
    main_interface,
    dbc.Row(dbc.Col((tabs))),
    html.Div(id='dummy'),
])
