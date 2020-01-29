VERSION 0.8

Primary Change: Command Queueing
Changes:
Remembered to update changelog


FUNCTIONALITY:
Bot now queues commands that are run for long lasting AHK scripts. Running Freeze, then BlockInput should properly run them in order and detect both commands in order, even if both of them take 10 seconds.

Bot will now copy all the included scripts into UserScripts when it generates that folder. Doesn't copy anything with .ahk in the name, but those are all in /IntRX/Resources/Included Scripts

Typing just a name into "File name to run" without an extension will now FIRST try .exe, and if it doesn't find it it tries .ahk, THEN says it cant find the file.

COMMANDS:
No changes or new commands
