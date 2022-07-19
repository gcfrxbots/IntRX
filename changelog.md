# VERSION 1.0 Casterlabs

Primary Change: Casterlabs Integration

**INTERACTION:**

Add DEFAULT ARG to add the option to not require an ARG for any command with %ARGS% - Instead it will automatically substitute in a value of your choice.

Added support for Subnautica Below Zero since it functions the exact same as basegame


**FUNCTIONALITY:**

Reworked authentication to be much more seamless. Bot will launch authentication popups to auth, thats it.

IntRX now has connectivity to all major streaming platforms, not just Twitch.

Authentication will automatically adapt to whatever the PLATFORM setting is configured to.

Added Authenticate.bat to add an easy way to auth, or it will run automatically on setup.

Remove REFRESH INTERVAL setting and just permanently set it to 2s. It doesnt really ever need to change from that and doesn't cause any performance hit.

