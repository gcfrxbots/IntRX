#VERSION 0.9

Primary Change: InteractConfig Scripting

INTERACTION:
Created a custom scripting format to be used within the InteractConfig!
Use $PRESS (Key), $HOLD (Key) (Seconds), $SPAM (Key) (Keypresses), $TYPE (String), $WAIT (Seconds), $CHAT (Message) and $RUN (Path) instead of just specifying an executable to run.
These can be chained together, and they're run in order from left to right.
Use %ARGS% in place of any of the variables (Like $TYPE %ARGS%) to use anything the user in chat specifies (If !command test, "test" is the args.)
Use %USER% as another variable, to display the username of the person who typed the command.
Bot runs automatic checks to ensure the commands are formatted correctly before loading them.

(0.9.2) - %ARGS% and %USER% can now be used in all games in their "Command to run" fields.
(0.9.3) - Fixed allowing %ARGS% to be in the place of a number for $HOLD and $SPAM


FUNCTIONALITY:
"File name to run" in InteractConfig is now called "What to Run", to support new built-in commands.  If you're updating from a previous version, this won't change, but will still work fine either way.
Bot now has a startup message encouraging users to support development
Cleaned up startup quite a bit
Changed how cooldowns work. The bot now displays the cooldown message for whatever has the highest cooldown, rather than always prioritizing Global.

