import os
try:
    import pandas as pd
    import xlsxwriter
    from system_hotkey import SystemHotkey, SystemRegisterError
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")


if not os.path.exists('Config'):
    os.mkdir("Config")

'''----------------------SETTINGS----------------------'''

'''FORMAT ---->   ("Option", "Default", "This is a description"), '''
settings = [
    ("Test", "True", "This is a test for the default setting Test"),
    ("Test2", "Banana", "Here I am testing Test2"),

]
'''----------------------END SETTINGS----------------------'''

if not os.path.exists('Config/Settings.xlsx'):
    # Create spreadsheet for settings using panda
    print("Creating Settings.xlsx")

    with xlsxwriter.Workbook('Config/Settings.xlsx') as workbook:  # FORMATTING
        worksheet = workbook.add_worksheet('Settings')
        format = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'gray'})
        boldformat = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'black'})
        lightformat = workbook.add_format({'center_across': True, 'font_color': 'black', 'bg_color': '#DCDCDC', 'border': True})
        worksheet.set_column(0, 0, 20)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 130)
        worksheet.write(0, 0, "Option", format)
        worksheet.write(0, 1, "Your Setting", boldformat)
        worksheet.write(0, 2, "Description", format)
        worksheet.set_column('B:B', 20, lightformat)  # END FORMATTING

        row = 1
        col = 0

        for option, default, description in settings:
            worksheet.write(row,  col, option)
            worksheet.write(row,  col + 1, default)
            worksheet.write(row,  col + 2, description)
            row += 1



# TODO - Read the file



## Check Settings
#print("Verifying Settings.py is set up correctly...")
#if PORT not in (80, 6667, 443, 6697):
#    raise ConnectionError("Wrong Port! The port must be 80 or 6667 for standard connections, or 443 or 6697 for SSL")
#if not BOT_OAUTH:
#    raise Exception("Missing BOT_OAUTH - Please follow directions in the settings or readme.")
#if not ('oauth:' in BOT_OAUTH):
#    raise Exception("Invalid BOT_OAUTH - Your oauth should start with 'oauth:'")
#if not BOT_NAME or not CHANNEL:
#    raise Exception("Missing BOT_NAME or CHANNEL - Please follow directions in the settings or readme")
#
#
#if ENABLE_HOTKEYS:
#    for item in HOTKEYS:
#        assignedKey = HOTKEYS[item]
#        if type(assignedKey) != tuple:
#            raise Exception('''Hotkeys formatted incorrectly! If you have just one key (no modifiers), it should look like >> "!veto": ('key',),''')
#        if len(assignedKey) < 1:
#            raise Exception("Hotkeys are enabled, but one or more hotkeys are not set. The bot can still run like this but an error will be thrown on startup.")
#