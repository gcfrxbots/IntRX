import os
try:
    import xlrd
    import pyperclip
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")

def importGlobal():
    globalCommands = []
    # Read the settings file
    wb = xlrd.open_workbook('../Config/InteractConfig.xlsx')
    sheet = wb.sheet_by_name("Global")
    for item in range(sheet.nrows):
        if item == 0:
            pass
        else:
            chatcmd = sheet.cell_value(item,0)
            cooldown = sheet.cell_value(item,1)
            disable = sheet.cell_value(item, 2)
            activewindow = sheet.cell_value(item, 3)
            ahkpath = sheet.cell_value(item, 4)

            if not cooldown:
                cooldown = 0.0

            if not disable.lower() in ['yes', 'true', 'disable', 'off']:
                if not chatcmd[0] == "!":  # Append ! to the command if it isnt there
                    chatcmd = "!" + chatcmd

                if "." not in ahkpath[4:]:  # Append .exe onto the end if it isnt there
                    ahkpath += ".exe"

                if not os.path.exists("../Config/UserScripts/" + ahkpath):
                    print("File %s does not exist, so the command %s was not added." % (ahkpath, chatcmd))
                else:
                    globalCommands.append((chatcmd, cooldown, ahkpath, activewindow))
    print("Loaded " + str(len(globalCommands)) + " global commands.")
    return globalCommands



def importInteraction(activeGame):
    interactCommands = []
    # Read the settings file
    wb = xlrd.open_workbook('../Config/InteractConfig.xlsx')
    sheet = wb.sheet_by_name(activeGame)
    for item in range(sheet.nrows):
        if item == 0:
            pass
        else:
            chatcmd = sheet.cell_value(item, 0)
            cooldown = sheet.cell_value(item, 1)
            disable = sheet.cell_value(item, 2)
            gamecmd = sheet.cell_value(item, 3)

            if not cooldown:
                cooldown = 0.0

            if not disable.lower() in ['yes', 'true', 'disable']:
                if not chatcmd[0] == "!":
                    chatcmd = "!" + chatcmd
                interactCommands.append((chatcmd, cooldown, gamecmd))
    print("Loaded " + str(len(interactCommands)) + " commands for " + activeGame)
    return interactCommands


class InteractGame:
    def __call__(self, activeGame, cmdToRun, cooldown, args, user):
        # Pass the command to a function, depending on the activeGame
        if activeGame in ['Skyrim', 'Fallout 4', 'Fallout NV', 'Oblivion', 'Fallout 3']:
            self.Bethesda(cmdToRun)
        elif activeGame in ['Fallout 3', 'Fallout NV']:
            self.FO3(cmdToRun)
        elif activeGame == "Witcher 3":
            self.Witcher3(cmdToRun)
        else:
            eval("self.%s(cmdToRun)" % activeGame)

    def Minecraft(self, cmdToRun):
        if cmdToRun[0] == "/":
            cmdToRun = cmdToRun[1:]
        pyperclip.copy(cmdToRun)
        os.startfile('Resources\Minecraft.exe')

    def Subnautica(self, cmdToRun):
        pyperclip.copy(cmdToRun)
        os.startfile('Resources\Subnautica.exe')

    def Bethesda(self, cmdToRun):
        with open('Resources/cmd.txt', 'w') as f:
            for item in cmdToRun:
                if item == ' ':
                    f.write('Space\n')
                else:
                    f.write(item + "\n")
        os.startfile('Resources\Bethesda.exe')

    def FO3(self, cmdToRun):
        with open('Resources/cmd.txt', 'w') as f:
            for item in cmdToRun:
                if item == ' ':
                    f.write('Space\n')
                else:
                    f.write(item + "\n")
        os.startfile('Resources\FO3.exe')

    def Witcher3(self, cmdToRun):
        with open('Resources/cmd.txt', 'w') as f:
            for item in cmdToRun:
                if item == ' ':
                    f.write('Space\n')
                else:
                    f.write(item + "\n")
        os.startfile('Resources\Witcher3.exe')