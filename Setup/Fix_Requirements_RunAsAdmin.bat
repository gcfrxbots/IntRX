echo This script is to fix any requirements that might not be installed correctly. IT MUST BE RUN AS ADMIN!
pause

py -3.7 -m pip uninstall websocket -y
py -3.7 -m pip uninstall websocket-client -y

py -3.7 -m pip install websocket-client --user --no-warn-script-location

pause