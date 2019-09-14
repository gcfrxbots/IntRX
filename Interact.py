import time
try:
    import xlrd
    import pyperclip
    from ahk import AHK
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
    print("Loaded " + str(len(interactCommands)) + " commands for " + activeGame)
    return interactCommands


class InteractGame:
    def __init__(self, settings):
        self.ahk = AHK(executable_path=settings['AHK_PATH'])

    def __call__(self, activeGame, cmdToRun, cooldown, args, user):
        # Pass the command to a function, depending on the activeGame
        eval("self.%s(cmdToRun)" % activeGame)

    def Minecraft(self, cmdToRun):
        if cmdToRun[0] == "/":
            cmdToRun = cmdToRun[1:]
        self.ahk.send_input('/')
        pyperclip.copy(cmdToRun)
        self.ahk.send('^v')
        time.sleep(0.02)
        self.ahk.send('{Enter}')

    def Subnautica(self, cmdToRun):
        self.ahk.send('{Enter}')
        pyperclip.copy(cmdToRun)
        self.ahk.send('^v')
        time.sleep(0.02)
        self.ahk.send('{Enter}')
