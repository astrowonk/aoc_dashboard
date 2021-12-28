# Advent of Code Private Leaderboard in Dash
Dash app that loads and parses Advent of Code leadboard json

The app is [running live on my web site](https://marcoshuerta.com/dash/aoc/), go check it out there! Upload your own private leaderboard JSON and see it in action.

Uses `dcc.Upload` and `dcc.Store` to load and store JSON from the AoC API, which is then parsed into pandas dataframes and figures by my [aoc_scoreboard](https://github.com/astrowonk/aoc_scoreboard) module.

With the default config file, the app will display an upload widge to accept uploaded JSON. Create your own `config.py` file if you wish to change settings to use server-side JSON and disable upload. Similarly you can change the base_url via the config file if self-hosting.

Clickable column headers that link to the day's AoC problem and [bootstrap tooltips](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/tooltip/) are courtesy of the callable one can pass to modify the header row in my [Dash DataFrame Table](https://github.com/astrowonk/dash_dataframe_table) module, so if you want to deploy this yourself, you'll need to install that module as well.


Things to do:

* Improve upon the rudimentary layout. Tabs may not be the best way to organize things.

* If the data store is empty/missing an upload, show some sort of example data. (or perhaps a "load example data" button...)


# Sample Images

## Day by Day Leaderboard
<img width="1201" alt="Screen Shot 2021-12-17 at 8 24 17 PM" src="https://user-images.githubusercontent.com/13702392/146624328-51e128ed-a12c-441f-b444-ace2f093a3fa.png">

## Score Line Graph
<img width="1225" alt="Screen Shot 2021-12-17 at 8 24 23 PM" src="https://user-images.githubusercontent.com/13702392/146624343-773f433c-d2e0-46b9-9abd-0a0cb2af6a97.png">

## Minutes between Stars Table

<img width="1221" alt="Screen Shot 2021-12-17 at 8 24 27 PM" src="https://user-images.githubusercontent.com/13702392/146624361-5e218d70-4084-4921-a39f-302347a78122.png">
