echo You need to have Python 3.7 (and the included PIP package) installed for this to work! Click OK to install all required packages.
pause


py -3.7 -m pip install -r requirements.txt --user --no-warn-script-location

py -3.7 ../IntRX/Initialize.py --g
py -3.7 ../IntRX/Authenticate.py

pause