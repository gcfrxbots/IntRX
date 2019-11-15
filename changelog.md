
DevLog:

11/14 lmao:

I've been doing a great job at keeping up with this changelog, clearly.
From here on out, changelogs will be handled like rxbot's. 

STILL 9/21 because last night's changes were at 3am:

Cooldowns work! Individual cooldowns for every command, configurable from the spreadsheet.

The AHK Library for python is no longer needed since AHK is all external.

AHK Scripts will need to be run as admin.

FO3/NV are now fully functional. Script works the same way but just needed a slightly longer delay.



Also 9/21

Made a quick fix to make every bethesda game use the same function and script. Skyrim, FO4, and Oblivion work.

FONV seems to work about half the time, so I'll make a new script for it a bit later to make sure it works consistently.

I can't for the life of me get FO3 to start, but I assume it's the exact same as NV.


9/21

Interaction ACTUALLY works! Untested for Oblivion and FO3 because I dont feel like setting them up, but everything else is working great!

Created a Resources folder that does NOT auto generate, as it has all the AHK files in it. Will keep AHK source files included.

Interaction uses AHK scripts now rather than the python AHK lib. MUCH faster and blockinput works.

Currently all interaction commands should be under 200ms per command executed, which is amazing imo.

9/14

Interaction actually works! Well, it does for Minecraft and Subnautica. Try it out!

Bot can now run commands per game, and evaluate which game's controller to send commands to.

Added a AHK_PATH setting for the path to your AutoHotkey.exe. This is only needed if AHK isn't in your environmental variables path.

Reformatted the settings xlsx a bit.

Added an error catcher for when people try to run commands without the bot detecting an active game yet.

Bot will now generate the Config files on first startup, then CLOSE so it doesn't throw any errors.

Lot of good stuff with this update! Will hopefully get bethsoft games working soon!


------------
9/10

Wow, has it really been this long since I made any update?

Bot can now detect when a loaded command is run, depending on the current game.

Created a class InteractGame which will eventually house all of the code for each specific game's input methods.

------------
9/3
Bot now determines if you've changed supported games, and loads config accordingly.

Added a setting to announce when you change supported games.

Bot now successfully loads all configured interaction commands from InteractConfig.xlsx, depending on which game is active.

Bot will not constantly refresh settings to save memory. Might add a setting for this in the future.

Need to add a setting for how quickly the game detector refreshes. Currently 3s default.

------------
9/2

Settings is reading perfectly and updating successfully.

Bot now creates InteractConfig where all commands will take place

Bot now detects your active window, and if your game is active it'll set activeGame to whatever that game is.

------------
8/31

ReadSettings is 60% of the way there

Everything else is blank or copypastes of rxbot3.
