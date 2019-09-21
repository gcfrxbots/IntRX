import urllib, urllib.request
import json
import socket
import os
try:
    import xlrd
    import xlsxwriter
    from system_hotkey import SystemHotkey, SystemRegisterError
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")



'''----------------------SETTINGS----------------------'''

'''FORMAT ---->   ("Option", "Default", "This is a description"), '''
defaultSettings = [
    ("PORT", "80", "Try 6667 if this doesn't work. Use 443, 6697 for SSL. Don't touch otherwise."),
    ("BOT_OAUTH", "", "To get this Oauth, head to https://twitchapps.com/tmi/ and log in with YOUR BOT'S ACCOUNT!"),
    ("BOT_NAME", "", "The twitch username of your bot (Lowercase)"),
    ("CHANNEL", "", "The twitch username of the channel you are connecting to (Lowercase)"),
    ("", "", ""),
    ("ANNOUNCE_GAME", "False", "Announce in chat when you begin playing a game that the bot supports. (TRUE / FALSE"),
    ("AHK_PATH", "C:/Program Files/AutoHotkey/AutoHotkey.exe", "The location of your AutoHotkey.exe"),
]
'''----------------------END SETTINGS----------------------'''


def formatSettingsXlsx():
    try:
        with xlsxwriter.Workbook('Config/Settings.xlsx') as workbook:  # FORMATTING
            worksheet = workbook.add_worksheet('Settings')
            format = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'gray'})
            boldformat = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'black'})
            lightformat = workbook.add_format({'center_across': True, 'font_color': 'black', 'bg_color': '#DCDCDC', 'border': True})
            worksheet.set_column(0, 0, 25)
            worksheet.set_column(1, 1, 50)
            worksheet.set_column(2, 2, 130)
            worksheet.write(0, 0, "Option", format)
            worksheet.write(0, 1, "Your Setting", boldformat)
            worksheet.write(0, 2, "Description", format)
            worksheet.set_column('B:B', 50, lightformat)  # END FORMATTING

            row = 1  # WRITE SETTINGS
            col = 0
            for option, default, description in defaultSettings:
                worksheet.write(row,  col, option)
                worksheet.write(row,  col + 1, default)
                worksheet.write(row,  col + 2, description)
                row += 1
        print("Settings.xlsx has been configured successfully.")
    except PermissionError:
        print("Can't open the settings file. Please close it and make sure it's not set to Read Only")

def formatInteractxlsx():
    try:
        with xlsxwriter.Workbook('Config/InteractConfig.xlsx') as workbook:  # FORMATTING
            listGames = ("Skyrim", "Oblivion", "Fallout4", "FalloutNV", "Fallout3", "Minecraft", "Subnautica")
            for item in listGames:
                worksheet = workbook.add_worksheet(item)
                format = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'gray'})
                lightformat = workbook.add_format({'center_across': True, 'font_color': 'black', 'bg_color': '#DCDCDC', 'border': True})
                worksheet.set_column(0, 0, 30)
                worksheet.set_column(1, 1, 30)
                worksheet.set_column(2, 2, 130)
                worksheet.write(0, 0, "Command", format)
                worksheet.write(0, 1, "Cooldown (Sec)", format)
                worksheet.write(0, 2, "Command To Execute", format)
                worksheet.set_column('B:B', 20, lightformat)  # END FORMATTING


        print("Config.xlsx has been updated successfully.")
    except PermissionError:
        print("Can't open the settings file. Please close it and make sure it's not set to Read Only")


def initSetup():
    global settings
    settings = {}
    if not os.path.exists('Config'):
        print("Creating a Config folder, check it out!")
        os.mkdir("Config")

    if not os.path.exists('Config/Settings.xlsx'):
        print("Creating Settings.xlsx")
        formatSettingsXlsx()
        print("\nPlease open Config / Settings.xlsx and configure the bot, then run it again.")
        quit()

    if not os.path.exists('Config/InteractConfig.xlsx'):
        print("Creating InteractionConfig.xlsx")
        formatInteractxlsx()

    # Read the settings file
    wb = xlrd.open_workbook('Config/Settings.xlsx')
    sheet = wb.sheet_by_name("Settings")
    for item in range(sheet.nrows):
        if item == 0:
            pass
        else:
            option = sheet.cell_value(item,0)
            setting = sheet.cell_value(item,1)
            settings[option] = setting

    # Check for new/changed settings
    if sheet.nrows != (len(defaultSettings)+1):
        print("The settings for IntRX have changed since you last started the script. Settings.xlsx has updated, go check it out.")

        for item in settings:
            for i in enumerate(defaultSettings):
                if (i[1][0]) == item:
                    defaultSettings[i[0]] = (item, settings[item], defaultSettings[i[0]][2])
        formatSettingsXlsx()

    # Check Settings
    if str(int(settings["PORT"])) not in ('80', '6667', '443', '6697'):  # Convert into non-float string
        raise ConnectionError("Wrong Port! The port must be 80 or 6667 for standard connections, or 443 or 6697 for SSL")
    if not settings['BOT_OAUTH']:
        raise Exception("Missing BOT_OAUTH - Please follow directions in the settings or readme.")
    if not ('oauth:' in settings['BOT_OAUTH']):
        raise Exception("Invalid BOT_OAUTH - Your oauth should start with 'oauth:'")
    if not settings['BOT_NAME'] or not settings['CHANNEL']:
        raise Exception("Missing BOT_NAME or CHANNEL - Please follow directions in the settings or readme")

    print(">> Initial Checkup Complete! Connecting to Chat...")
    return settings

def openSocket():
    global settings
    global s
    s = socket.socket()
    s.connect(("irc.chat.twitch.tv", int(settings["PORT"])))
    s.send(("PASS " + settings["BOT_OAUTH"] + "\r\n").encode("utf-8"))
    s.send(("NICK " + settings["BOT_NAME"] + "\r\n").encode("utf-8"))
    s.send(("JOIN #" + settings["CHANNEL"] + "\r\n").encode("utf-8"))
    return s


def sendMessage(message):
    global settings
    messageTemp = "PRIVMSG #" + settings["CHANNEL"] + " : " + message
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
        print(">> IntRX Startup complete!")
        return False
    else:
        return True



def getmoderators():
    global settings
    json_url = urllib.request.urlopen('http://tmi.twitch.tv/group/user/' + settings("CHANNEL").lower() + '/chatters')

    data = json.loads(json_url.read())
    mods = data['chatters']['moderators']

#    for item in mods:
#        if mods not in MODERATORS:
#            MODERATORS.append(item)
#
#    return MODERATORS

