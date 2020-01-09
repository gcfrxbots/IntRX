from Initialize import *
from Interact import importInteraction, InteractGame, importGlobal
import datetime
import re
import time
from threading import Thread
from win32gui import GetWindowText, GetForegroundWindow

settings = initSetup()
interact = InteractGame()
currentCommands = False


class antiCommand:  # Anticommands, my name for grabbing the command from a chat message rather than a command.
    def __init__(self):
        self.fromLeft = 0
        self.fromRight = 0
        self.leftStr = ""
        self.rightStr = ""

    def trimSetting(self):
        if settings["COMMAND PHRASE"]:
            phrase = settings["COMMAND PHRASE"].lower()
            self.fromLeft = 0
            self.fromRight = 0
            self.leftStr = phrase.split("%cmd%", 1)[0]
            self.rightStr = phrase.split("%cmd%", 1)[1]
            if len(self.leftStr) < 3:
                stopBot("Your setting for COMMAND PHRASE is too short. You need at least 4 characters before %cmd%. ")
            self.fromLeft = len(self.leftStr)
            self.fromRight = len(self.rightStr)
            return self.leftStr  # Left side of the message includes the

    def extractCmd(self, cmd):
        cmd = (cmd.replace("\r", '').strip()).lower()
        toreturn = ""
        cmd = (self.leftStr + cmd.split(self.leftStr, 1)[1])

        if self.fromLeft and self.fromRight:
            toreturn = cmd[self.fromLeft:-self.fromRight]
        elif self.fromLeft:
            toreturn = cmd[self.fromLeft:]
        elif self.fromRight:
            toreturn = cmd[:-self.fromRight]

        print(toreturn)
        return toreturn.replace("!", '')


antiCmd = antiCommand()

def getUser(line):
    seperate = line.split(":", 2)
    user = seperate[1].split("!", 1)[0]
    return user


def getMessage(line):
    seperate = line.split(":", 2)
    message = seperate[2]
    return message


def formatted_time():
    return datetime.datetime.today().now().strftime("%I:%M")


def getint(cmdarguments):
    try:
        out = int(re.search(r'\d+', cmdarguments).group())
        return out
    except:
        return None


def writeArgs(args):
    args = args.replace('\r', '')
    with open("../Config/UserScripts/output.txt", "w") as f:
        f.write(args)


def runCmdExtras(command, cmdarguments, item):
    tempCooldown = datetime.datetime.now() + datetime.timedelta(seconds=item[1])
    tempGlobalCooldown = datetime.datetime.now() + datetime.timedelta(seconds=settings["CD BETWEEN CMDS"])
    cooldowns.update({command: tempCooldown})
    cooldowns.update({"00rx_globalCD": tempGlobalCooldown})
    writeArgs(cmdarguments)
    print(item[0] + " executed!")


def runcommand(command, cmdarguments, user):
    global currentCommands, activeGame, cooldowns, globalCommands
    if not currentCommands:
        currentCommands = []
    run = False
    for item in currentCommands, globalCommands:
        for i in item:
            if command.lower() == i[0].lower():
                run = True

    if run:
        # Manage cooldowns
        if "00rx_globalCD" in cooldowns.keys():  # This is just weird so theres no way anyone will ever accidentally have their command say this. Note, if your command says this and you ask for help, ill be pissed.
            timeleft = cooldowns["00rx_globalCD"] - datetime.datetime.now()
            timeleftSecs = round(timeleft.total_seconds())
            if timeleftSecs == 0:
                pass
            else:
                sendMessage("Since a command was run recently, nobody can interact for %s more seconds." % timeleftSecs)
                return

        if command in cooldowns.keys():
            timeleft = cooldowns[command] - datetime.datetime.now()
            timeleftSecs = round(timeleft.total_seconds())
            if timeleftSecs > 1 and (str(timeleft) != "-1"):
                sendMessage("That command is still on cooldown for %s seconds." % timeleftSecs)
                return

        for item in currentCommands:  # Test if the command run is for a loaded game
            if command.lower() == item[0].lower():  # Command detected, pass this to the InteractGame class.
                interact(activeGame, item[2], item[1], cmdarguments, user)
                runCmdExtras(command, cmdarguments, item)
                return

        for item in globalCommands:  # Test if command run is a global command
            if command.lower() == item[0].lower():  # Command detected, run the file

                if item[3]:  # Do this stuff if there's a specified active window
                    if item[3] in GetWindowText(GetForegroundWindow()):
                        os.startfile(r"..\Config\UserScripts\\" + item[2])
                        runCmdExtras(command, cmdarguments, item)
                        return

                else:  # Otherwise just active the command
                    os.startfile(r"..\Config\UserScripts\\" + item[2])
                    runCmdExtras(command, cmdarguments, item)
                    return


def main():
    global globalCommands
    globalCommands = importGlobal()
    s = openSocket()
    joinRoom(s)
    readbuffer = ""
    while True:
        readbuffer = readbuffer + s.recv(1024).decode("utf-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()
        for line in temp:
            if "PING" in line:
                s.send(bytes("PONG :tmi.twitch.tv\r\n".encode("utf-8")))
            else:
                # All these things break apart the given chat message to make things easier to work with.
                user = getUser(line)
                message = str(getMessage(line))
                command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
                cmdarguments = message.replace(command or "\r" or "\n", "")[1:]
                getint(cmdarguments)
                print(("(" + formatted_time() + ")>> " + user + ": " + message))
                # Run the commands function

                if settings["COMMAND PHRASE"]:  # Process anticommands
                    if user in [settings["BOT NAME"], settings["ALT BOT NAME"]]:
                        if antiCmd.trimSetting() in message.lower():
                            extractedCmd = antiCmd.extractCmd(message)
                            cmdarguments = (extractedCmd.replace(extractedCmd.split(" ")[0], '')).strip()
                            toRun = extractedCmd.split(" ")[0]
                            print("Running command from another bot: " + toRun)
                            runcommand("!" + toRun, cmdarguments, user)

                elif command[0] == "!":  # Only run normal commands if COMMAND PHRASE is blank
                    runcommand(command, cmdarguments, user)


supportedGames = {
    # Window Name : Function Name
    "Skyrim Special Edition": "Skyrim",
    "Oblivion": "Oblivion",
    "Fallout4": "Fallout 4",
    "Fallout: New Vegas": "Fallout NV",
    "Fallout3": "Fallout 3",
    "Minecraft": "Minecraft",
    "Subnautica": "Subnautica",
    "The Witcher 3": "Witcher 3"
}


def refresh():
    global currentCommands, activeGame
    cacheActiveGame = ''
    activeGame = None
    while True:
        time.sleep(int(settings['REFRESH INTERVAL']))
        currentWindow = GetWindowText(GetForegroundWindow())

        activeGame = None

        for winName in supportedGames:
            if winName in currentWindow and (activeGame != supportedGames[winName]):
                activeGame = supportedGames[winName]

        if cacheActiveGame != activeGame and activeGame:  # Do when user starts NEW game
            print("Now playing " + activeGame)
            cacheActiveGame = activeGame
            if settings['ANNOUNCE GAME'].lower() == "yes":
                sendMessage("The streamer is now playing " + activeGame + " and you can interact with it!")
            currentCommands = importInteraction(activeGame)

        elif not activeGame:  # If no game is loaded
            currentCommands = []

        elif activeGame and (len(currentCommands) == 0):  # If the game is tabbed back in, but not a new game (don't announce it)
            currentCommands = importInteraction(activeGame)


def tick():
    global cooldowns
    cooldowns = {}
    while True:
        time.sleep(0.5)
        if cooldowns:
            for item in cooldowns:
                if cooldowns[item] <= datetime.datetime.now():
                    cooldowns.pop(item)
                    break


t1 = Thread(target = main)
t2 = Thread(target = refresh)
t3 = Thread(target = tick)


t1.start()
t2.start()
t3.start()

