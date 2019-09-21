from Initialize import *
from Interact import ImportSettings, InteractGame
import datetime
import re
import time
from threading import Thread
from win32gui import GetWindowText, GetForegroundWindow

settings = initSetup()
interact = InteractGame(settings)
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
    except: return None


def runcommand(command, cmdarguments, user):
    global currentCommands, activeGame
    if not currentCommands:
        print("No game is currently loaded.")
        return
    for item in currentCommands:
        if command == item[0]:  # Command detected, pass this to the InteractGame class.
            interact(activeGame, item[2], item[1], cmdarguments, user)
            print(item[0] + " executed!")



def main():
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

def refresh():
    global currentCommands, activeGame
    activeGame = ""
    while True:
        time.sleep(3)
        currentWindow = GetWindowText(GetForegroundWindow())
        gameUpdated = False
        if currentWindow == "Skyrim Special Edition" and (activeGame != "Skyrim"):
            activeGame = "Skyrim"
            gameUpdated = True
        if currentWindow == "Oblivion" and (activeGame != "Oblivion"):
            activeGame = "Oblivion"
            gameUpdated = True

        if currentWindow == "Fallout4" and (activeGame != "Fallout4"):
            activeGame = "Fallout4"
            gameUpdated = True
        if currentWindow == "Fallout: New Vegas" and (activeGame != "FalloutNV"):
            activeGame = "FalloutNV"
            gameUpdated = True
        if currentWindow == "Fallout3" and (activeGame != "Fallout3"):
            activeGame = "Fallout3"
            gameUpdated = True

        if currentWindow[:9] == "Minecraft" and (activeGame != "Minecraft"):
            activeGame = "Minecraft"
            gameUpdated = True
        if currentWindow == "Subnautica" and (activeGame != "Subnautica"):
            activeGame = "Subnautica"
            gameUpdated = True

        if gameUpdated == True:  # Do these things when the user starts playing a new game.
            print("Now playing " + activeGame)
            if settings['ANNOUNCE_GAME']:
                sendMessage("The streamer is now playing " + activeGame + " and you can interact with it!")
            currentCommands = ImportSettings(activeGame)

t1 = Thread(target = main)
t2 = Thread(target = refresh)


t1.start()
t2.start()

