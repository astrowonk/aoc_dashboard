# Advent of Code Private Leaderboard in Dash
Dash app that loads and parses Advent of Code leadboard json

Uses `dcc.Upload` and `dcc.Store` to load and store JSON from the AoC API, which is then parsed into pandas dataframes and figures by my [aoc_scoreboard](https://github.com/astrowonk/aoc_scoreboard) module.

The app will use the default config and accept uploaded JSON. Create your own `config.py` file if you wish to change settings
or use server-side JSON and disable upload.

The app is [running live on my web site](https://marcoshuerta.com/dash/aoc/), go check it out there!

Things to do:

* Improve upon the very rudimentary layout. Not sure tabs are the best way to organize things.
