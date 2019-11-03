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


def runcommand(command, cmdarguments, user):
    global currentCommands, activeGame, cooldowns, globalCommands
    if not currentCommands:
        currentCommands = []
    if command in cooldowns.keys():
        timeleft = cooldowns[command] - datetime.datetime.now()
        timeleftSecs = round(timeleft.total_seconds())
        if timeleftSecs == 0:
            pass
        else:
            sendMessage("That command is still on cooldown for %s seconds." % timeleftSecs)
            return

    for item in currentCommands:  # Test if the command run is for a loaded game
        if command == item[0]:  # Command detected, pass this to the InteractGame class.
            interact(activeGame, item[2], item[1], cmdarguments, user)
            tempCooldown = datetime.datetime.now() + datetime.timedelta(seconds=item[1])
            cooldowns.update({command: tempCooldown})
            print(item[0] + " executed!")
            return

    for item in globalCommands:  # Test if command run is a global command
        if command == item[0]:  # Command detected, run the file
            os.startfile(r"..\Config\UserScripts\\" + item[2])
            tempCooldown = datetime.datetime.now() + datetime.timedelta(seconds=item[1])
            cooldowns.update({command: tempCooldown})
            print(item[0] + " executed!")
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
                cmdarguments = message.replace(command or "\r" or "\n", "")
                getint(cmdarguments)
                print(("(" + formatted_time() + ")>> " + user + ": " + message))
                # Run the commands function
                if command[0] == "!":
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
}


def refresh():
    global currentCommands, activeGame
    activeGame = ""
    cacheActiveGame = ''
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

