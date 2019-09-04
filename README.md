# IntRX
Dynamic Live In-Game Interaction for Twitch Chat

DevLog:

9/3
Bot now determines if you've changed supported games, and loads config accordingly.
Added a setting to announce when you change supported games.
Bot now successfully loads all configured interaction commands from InteractConfig.xlsx, depending on which game is active.
Bot will not constantly refresh settings to save memory. Might add a setting for this in the future.
Need to add a setting for how quickly the game detector refreshes. Currently 3s default.

9/2
Settings is reading perfectly and updating successfully.
Bot now creates InteractConfig where all commands will take place
Bot now detects your active window, and if your game is active it'll set activeGame to whatever that game is.


8/31
ReadSettings is 60% of the way there
Everything else is blank or copypastes of rxbot3.
