
try:
    import xlrd
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")



def ImportSettings(activeGame):
    interactCommands = []
    # Read the settings file
    wb = xlrd.open_workbook('Config/InteractConfig.xlsx')
    sheet = wb.sheet_by_name(activeGame)
    for item in range(sheet.nrows):
        if item == 0:
            pass
        else:
            chatcmd = sheet.cell_value(item,0)
            cooldown = sheet.cell_value(item,1)
            gamecmd = sheet.cell_value(item,2)
            interactCommands.append((chatcmd, cooldown, gamecmd))
    print(interactCommands)