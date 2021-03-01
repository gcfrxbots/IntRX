import os
import time
from Initialize import *
try:
    import xlrd
    import pyperclip
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")

settings = initSetup()

def writeArgs(args):
    args = args.replace('\r', '')
    with open("../Config/UserScripts/output.txt", "w") as f:
        f.write(args)


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
            activeWindow = sheet.cell_value(item, 3)
            whatToRun = sheet.cell_value(item, 4)

            if not cooldown:
                cooldown = 0.0

            if not disable.lower() in ['yes', 'true', 'disable', 'off']:
                if chatcmd:  # Prevents errors if there's no chat command specified
                    if not chatcmd[0] == "!":  # Append ! to the command if it isnt there
                        chatcmd = "!" + chatcmd

                    if whatToRun[0] == "$":
                        if checkGlobalBuiltInScripts(chatcmd, whatToRun):
                            globalCommands.append((chatcmd, cooldown, whatToRun, activeWindow))
                    else:
                        if "." not in whatToRun:  # Append .exe onto the end if it isnt there
                            whatToRun += ".exe"

                        if not os.path.exists("../Config/UserScripts/" + whatToRun):
                            whatToRun = whatToRun[:-4] + ".ahk"

                        if not os.path.exists("../Config/UserScripts/" + whatToRun):
                            print("File %s does not exist, so the command %s was not added." % (whatToRun, chatcmd))
                        else:
                            globalCommands.append((chatcmd, cooldown, whatToRun, activeWindow))
                else:  # No cmd specified
                    print("An entry in your InteractConfig Global page doesn't have a Command specified, so it wasn't loaded.")
                    time.sleep(2)

    print(">> Loaded " + str(len(globalCommands)) + " global commands.")
    return globalCommands

def isValidInt(strInput):
    if strInput.strip() == "%ARGS%":
        return True
    else:
        try:
            int(strInput)
            return True
        except ValueError:
            return False

def checkGlobalBuiltInScripts(chatcmd, whatToRun):
    allCommands = whatToRun.split("$")[1:]
    for fullCmd in allCommands:
        fullCmd = fullCmd.split(" ")
        while "" in fullCmd:
            fullCmd.remove("")
        command = fullCmd[0]
        success = False
        if command == "PRESS":  # $PRESS G
            if len(fullCmd) == 2:
                if type(fullCmd[1]) == str:
                    success = True
        if command == "HOLD":  # $HOLD G 10 (Hold G for 10 seconds)
            if len(fullCmd) == 3:
                if type(fullCmd[1]) == str and isValidInt(fullCmd[2]):
                    success = True
        if command == "SPAM":  # SPAM G 5 (Spam G 5 times)
            if len(fullCmd) == 3:
                if type(fullCmd[1]) == str and isValidInt(fullCmd[2]):
                    success = True
        if command == "TYPE":  # TYPE String
            if len(fullCmd) >= 2:
                if type(fullCmd[1]) == str:
                    success = True
        if command == "WAIT":  # WAIT 5 (Wait 5 seconds)
            if len(fullCmd) == 2:
                if isValidInt(fullCmd[1]):
                    success = True
        if command == "RUN":  # RUN Blockinput.exe (Any script from Userscripts folder)
            if len(fullCmd) == 2:
                fileName = fullCmd[1]
                if "." not in fileName:  # Append .exe onto the end if it isnt there
                    fileName += ".exe"
                if not os.path.exists("../Config/UserScripts/" + fileName):
                    fileName = fileName[:-4] + ".ahk"
                if not os.path.exists("../Config/UserScripts/" + fileName):
                    print("The file specified in %s does not exist!" % chatcmd)
                else:
                    success = True
        if command == "CHAT":  # TYPE String
            if len(fullCmd) >= 2:
                if type(fullCmd[1]) == str:
                    success = True

        if not success:
            print("Your global command %s could not be loaded, because it's What to Run field was formatted incorrectly." % chatcmd)
            time.sleep(2)
            return False
    return True


def processBuiltInGlobal(fullInteractCmd, cmdArguments, user):
    if "%ARGS%" in fullInteractCmd and not cmdArguments:
        return False

    commands = fullInteractCmd.split("$")
    while "" in commands:
        commands.remove("")
    for fullCmd in commands:
        # Replace the variables with their actual values
        arg = cmdArguments.replace("\r", "")
        fullCmd = fullCmd.replace("%ARGS%", arg)
        fullCmd = fullCmd.replace("%USER%", user)
        fullCmd = fullCmd.strip()
        cmd = fullCmd.split(" ")[0]
        args = fullCmd.replace(cmd, '').strip()
        writeArgs(args)

        if cmd == "PRESS":
            print("Pressing %s." % args)
            script.runAHK('Resources\PRESS.exe')
        if cmd == "HOLD":
            print("Holding %s for %s seconds." % (args.split(" ")[0], args.split(" ")[1]))
            script.runAHK('Resources\HOLD.exe')
        if cmd == "SPAM":
            print("Spamming %s %s times." % (args.split(" ")[0], args.split(" ")[1]))
            script.runAHK('Resources\SPAM.exe')
        if cmd == "TYPE":
            print("Typing %s." % args)
            script.runAHK('Resources\TYPE.exe')
        if cmd == "WAIT":
            print("Waiting %s seconds." % args)
            time.sleep(int(args))
        if cmd == "RUN":
            print("Running %s." % args)
            script.runAHK(r"..\Config\UserScripts\%s" % args)
        if cmd == "CHAT":
            print("Sending %s to chat." % args)
            print(args)
            sendMessage(args)
    return True


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
                if chatcmd:  # Prevents errors if there's no chat command specified
                    if not chatcmd[0] == "!":
                        chatcmd = "!" + chatcmd
                    interactCommands.append((chatcmd, cooldown, gamecmd))
                else:  # No cmd specified
                    print("An entry in your InteractConfig " + activeGame + " page doesn't have a Command specified, so it wasn't loaded.")
    print(">> Loaded " + str(len(interactCommands)) + " commands for " + activeGame)
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
        script.runAHK('Resources\Minecraft.exe')

    def Subnautica(self, cmdToRun):
        pyperclip.copy(cmdToRun)
        script.runAHK('Resources\Subnautica.exe')

    def Bethesda(self, cmdToRun):
        with open('Resources/cmd.txt', 'w') as f:
            for item in cmdToRun:
                if item == ' ':
                    f.write('Space\n')
                else:
                    f.write(item + "\n")
        script.runAHK('Resources\Bethesda.exe')

    def FO3(self, cmdToRun):
        with open('Resources/cmd.txt', 'w') as f:
            for item in cmdToRun:
                if item == ' ':
                    f.write('Space\n')
                else:
                    f.write(item + "\n")
        script.runAHK('Resources\FO3.exe')

    def Witcher3(self, cmdToRun):
        with open('Resources/cmd.txt', 'w') as f:
            for item in cmdToRun:
                if item == ' ':
                    f.write('Space\n')
                else:
                    f.write(item + "\n")
        script.runAHK('Resources\Witcher3.exe')

    def Valheim(self, cmdToRun):
        with open('Resources/cmd.txt', 'w') as f:
            for item in cmdToRun:
                if item == ' ':
                    f.write('Space\n')
                else:
                    f.write(item + "\n")
        script.runAHK('Resources\Valheim.exe')


class scriptTasking:
    def __init__(self):
        self.isScriptRunning = False
        self.scriptQueue = []

    def runAHK(self, path):
        if self.isScriptRunning:  # Queue the next thing to be run
            self.scriptQueue.append(path)
            return

        self.isScriptRunning = True
        os.system(path)
        self.isScriptRunning = False

        if self.scriptQueue:
            self.runAHK(self.scriptQueue[0])


script = scriptTasking()