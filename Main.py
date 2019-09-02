from Initialize import *
import datetime
import re
from threading import Thread

initSetup()

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
                        #runcommand(command, cmdarguments, user, False)
        except socket.error:
            print("Socket died")


t1 = Thread(target = main)


t1.start()

