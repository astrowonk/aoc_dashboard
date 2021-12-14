# Advent of Code Private Leaderboard in Dash
Dash app that loads and parses Advent of Code leadboard json

Uses `dcc.Upload` and `dcc.Store` to load and store JSON from the AoC API, which is then parsed into pandas dataframes and figures by [aoc_scoreboard](https://github.com/astrowonk/aoc_scoreboard).

The app is [running live on my web site](https://marcoshuerta.com/dash/aoc/), go check it out there!

Things to do:

* Improve the layout.
* Add additional charts / tables ([aoc_scoreboard](https://github.com/astrowonk/aoc_scoreboard) can compute time between stars but I don't have this plotted or in a chart yet here.)
* Add a configuration option to use a local .json file for anyone who wants to host an instance themselves.
  