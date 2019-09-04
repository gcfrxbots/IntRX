from Initialize import *
from Interact import ImportSettings
import datetime
import re
import time
from threading import Thread
from win32gui import GetWindowText, GetForegroundWindow

settings = initSetup()

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

    wb = xlrd.open_workbook('Config/Settings.xlsx')
    sheet = wb.sheet_by_name("Settings")
    for item in range(sheet.nrows):
        if item == 0:
            pass
        else:
            option = sheet.cell_value(item,0)
            setting = sheet.cell_value(item,1)
            settings[option] = setting


def main():
    s = openSocket()
    joinRoom(s)
    readbuffer = ""
    while True:
        try:
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
                        print("Command")
                        #runcommand(command, cmdarguments, user)
        except socket.error:
            print("Socket died")



def refresh():
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

        if currentWindow == "Fallout4" and (activeGame != "Fallout 4"):
            activeGame = "Fallout 4"
            gameUpdated = True
        if currentWindow == "Fallout: New Vegas" and (activeGame != "Fallout NV"):
            activeGame = "Fallout NV"
            gameUpdated = True
        if currentWindow == "Fallout3" and (activeGame != "Fallout 3"):
            activeGame = "Fallout 3"
            gameUpdated = True

        if currentWindow[:9] == "Minecraft" and (activeGame != "Minecraft"):
            activeGame = "Minecraft"
            gameUpdated = True
        if currentWindow == "Subnautica" and (activeGame != "Subnautica"):
            activeGame = "Subnautica"
            gameUpdated = True


        if gameUpdated == True:
            print("Now playing " + activeGame)
            if settings['ANNOUNCE_GAME']:
                sendMessage("The streamer is now playing " + activeGame + " and you can interact with it!")
            ImportSettings(activeGame)

t1 = Thread(target = main)
t2 = Thread(target = refresh)


t1.start()
t2.start()

