START CMD /C "ECHO You need to have Python 3.7 (and the included PIP package) installed for this to work! Press any key to install all required packages. && PAUSE"
pause



py -3.7 -m pip install -r requirements.txt --user --no-warn-script-location


cd ../IntRX

py -3.7 ../IntRX/Initialize.py --g


pause

