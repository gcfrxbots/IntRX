from ReadSettings import *
import urllib, urllib.request
import json
import socket
import os



def initSetup():

    # Create Folders
    if not os.path.exists('Output'):
        os.makedirs('Output')
    if not os.path.exists('Resources'):
        os.makedirs('Resources')
        print("Creating necessary folders...")


    # Check NowPlaying.txt
    with open("Output/NowPlaying.txt", "w") as f:
        f.truncate()








    print(">> Initial Checkup Complete! Connecting to Chat...")
    return api


def openSocket():
    global s
    s = socket.socket()
    s.connect(("irc.chat.twitch.tv", PORT))
    s.send(("PASS " + BOT_OAUTH + "\r\n").encode("utf-8"))
    s.send(("NICK " + BOT_NAME + "\r\n").encode("utf-8"))
    s.send(("JOIN #" + CHANNEL + "\r\n").encode("utf-8"))
    return s


def sendMessage(message):
    print(message)
    messageTemp = "PRIVMSG #" + CHANNEL + " : " + message
    s.send((messageTemp + "\r\n").encode("utf-8"))
    print("Sent: " + messageTemp)


def joinRoom(s):
    readbuffer = ""
    Loading = True

    while Loading:
        readbuffer = readbuffer + s.recv(1024).decode("utf-8")
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()

        for line in temp:
            print(line)
            Loading = loadingComplete(line)



def loadingComplete(line):
    if("End of /NAMES list" in line):
        print(">> Bot Startup complete!")
        return False
    else:
        return True


def sqliteread(command):
    db = sqlite3.connect('Resources/botData.db')
    try:
        cursor = db.cursor()
        cursor.execute(command)
        data = cursor.fetchone()
        db.close()
        return data
    except Error as e:
        db.rollback()
        print("SQLITE READ ERROR:")
        print(e)

def sqlitewrite(command):
    db = sqlite3.connect('Resources/botData.db')
    try:
        cursor = db.cursor()
        cursor.execute(command)
        data = cursor.fetchone()
        db.commit()
        db.close()
        createsongqueue()
        return data
    except Error as e:
        db.rollback()
        print("SQLITE WRITE ERROR:")
        print(e)



def createsongqueue():
    db = sqlite3.connect('Resources/botData.db')
    cursor = db.cursor()
    cursor.execute("SELECT id, name, song FROM queue")
    data = cursor.fetchall()
    # Write to the excel workbook
    row = 1
    col = 0
    try:
        with xlsxwriter.Workbook('Output/SongQueue.xlsx') as workbook:
            worksheet = workbook.add_worksheet('Queue')
            format = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'gray'})
            center = workbook.add_format({'center_across': True})
            worksheet.set_column(0, 0, 8)
            worksheet.set_column(1, 1, 30)
            worksheet.set_column(2, 2, 100)
            worksheet.write(0, 0, "ID", format)
            worksheet.write(0, 1, "User", format)
            worksheet.write(0, 2, "Title / Link", format)
            for id, name, song in (data):
                worksheet.write(row, col,   id, center)
                worksheet.write(row, col + 1, name, center)
                worksheet.write(row, col + 2, song)
                row += 1
    except IOError:
        print("ERROR - UNABLE TO READ XLSX DOC! You probably have it open, close it ya buffoon")



def getmoderators():
    json_url = urllib.request.urlopen('http://tmi.twitch.tv/group/user/' + CHANNEL.lower() + '/chatters')

    data = json.loads(json_url.read())
    mods = data['chatters']['moderators']

    for item in mods:
        if mods not in MODERATORS:
            MODERATORS.append(item)

    return MODERATORS

