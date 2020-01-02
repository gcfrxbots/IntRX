import socket
import os
import argparse
import time
from distutils.dir_util import copy_tree
try:
    import xlrd
    import xlsxwriter
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")

parser = argparse.ArgumentParser(description='Generate Settings File')
parser.add_argument('--g', dest="GenSettings", action="store_true")
parser.set_defaults(GenSettings=False)

GenSettings = (vars(parser.parse_args())["GenSettings"])

'''----------------------SETTINGS----------------------'''

'''FORMAT ---->   ("Option", "Default", "This is a description"), '''
defaultSettings = [
    ("PORT", "80", "Try 6667 if this doesn't work. Use 443, 6697 for SSL. Don't touch otherwise."),
    ("BOT OAUTH", "", "To get this Oauth, head to https://twitchapps.com/tmi/ and log in with YOUR BOT'S ACCOUNT!"),
    ("BOT NAME", "", "The twitch username of your bot (Lowercase)"),
    ("CHANNEL", "", "The twitch username of the channel you are connecting to (Lowercase)"),
    ("", "", ""),
    ("ANNOUNCE GAME", "Yes", "Announce in chat when you begin playing a game that the bot supports. (Yes/No)"),
    ("REFRESH INTERVAL", 5, "The period of time, in seconds, that the bot refreshes your active window to load or unload commands for a game."),
    ("CD BETWEEN CMDS", 15, "The cooldown, in seconds, between two consecutive commands."),
    ("", "", ""),
    ("ALT BOT NAME", "", "If you use another bot which uses its own Twitch account, such as NightBot or StreamElements, type its name here."),
    ("COMMAND PHRASE", "", "If this isn't empty, commands will only be accepted from your bot(s), and must be executed via this phrase. Use %cmd% to mark where the command goes. Check the site for more info."),
]
'''----------------------END SETTINGS----------------------'''


def stopBot(err):
    print(">>>>>---------------------------------------------------------------------------<<<<<")
    print(err)
    print("More info can be found here: https://rxbots.net/intrx-setup.html")
    print(">>>>>----------------------------------------------------------------------------<<<<<")
    time.sleep(3)
    quit()


def formatSettingsXlsx():
    try:
        with xlsxwriter.Workbook('../Config/Settings.xlsx') as workbook:  # FORMATTING
            worksheet = workbook.add_worksheet('Settings')
            format = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'gray'})
            boldformat = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'black'})
            lightformat = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'black', 'bg_color': '#DCDCDC', 'border': True})
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
        stopBot("Can't open the settings file. Please close it and make sure it's not set to Read Only")


def formatInteractxlsx():
    try:
        with xlsxwriter.Workbook('../Config/InteractConfig.xlsx') as workbook:  # FORMATTING
            listGames = ("Skyrim", "Oblivion", "Fallout 4", "Fallout NV", "Fallout 3", "Minecraft", "Subnautica")

            format = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'gray'})
            lightformat = workbook.add_format({'center_across': True, 'font_color': 'black', 'bg_color': '#DCDCDC', 'border': True})
            evenlighterformat =  workbook.add_format({'center_across': True, 'font_color': 'black', 'bg_color': '#f0f0f0', 'border': True})
            redformat = workbook.add_format({'font_color': 'black', 'bg_color': '#ffdede', 'border': True})

            worksheet = workbook.add_worksheet("Global")  # FORMAT GLOBAL
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 1, 10)
            worksheet.set_column(2, 2, 10)
            worksheet.set_column(3, 3, 45)
            worksheet.set_column(4, 4, 70)
            worksheet.write(0, 0, "Command", format)
            worksheet.write(0, 1, "Cooldown", format)
            worksheet.write(0, 2, "Disable", format)
            worksheet.write(0, 3, "Active Window", format)
            worksheet.write(0, 4, "File Name To Run", format)
            worksheet.set_column('B:B', 10, lightformat)
            worksheet.set_column('C:C', 10, redformat)
            worksheet.set_column('D:D', 45, evenlighterformat)

            for item in listGames:  # FORMAT GAMES
                worksheet = workbook.add_worksheet(item)
                worksheet.set_column(0, 0, 30)
                worksheet.set_column(1, 1, 10)
                worksheet.set_column(2, 2, 10)
                worksheet.set_column(3, 3, 130)
                worksheet.write(0, 0, "Command", format)
                worksheet.write(0, 1, "Cooldown", format)
                worksheet.write(0, 2, "Disable", format)
                worksheet.write(0, 3, "Command To Execute", format)
                worksheet.set_column('B:B', 10, lightformat)  # END FORMATTING
                worksheet.set_column('C:C', 10, redformat)  # END FORMATTING
            # Create Global Worksheet

        print("Config.xlsx has been updated successfully.")
    except PermissionError:
        stopBot("Can't open the settings file. Please close it and make sure it's not set to Read Only")


def initSetup():
    global settings
    settings = {}
    killbot = False
    if not os.path.exists('../Config'):
        os.mkdir("../Config")

    if not os.path.exists('../Config/UserScripts'):
        os.mkdir("../Config/UserScripts")

    if not os.path.exists("../Config/UserScripts/Templates"):
        copy_tree("./Resources/Templates", "../Config/UserScripts/Templates")

    if not os.path.exists('../Config/Settings.xlsx'):
        formatSettingsXlsx()
        killbot = True

    if not os.path.exists('../Config/InteractConfig.xlsx'):
        print("Creating InteractionConfig.xlsx")
        killbot = True
        formatInteractxlsx()

    if killbot:
        stopBot("\nPlease open the Config folder and edit Settings.xlsx by following the readme, then start the bot again.")

    # Read the settings file
    wb = xlrd.open_workbook('../Config/Settings.xlsx')
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
        for item in settings:
            for i in enumerate(defaultSettings):
                if (i[1][0]) == item:
                    defaultSettings[i[0]] = (item, settings[item], defaultSettings[i[0]][2])
        formatSettingsXlsx()
        stopBot("The settings for IntRX have changed since you last started the script. Settings.xlsx has updated, go check it out.")

    # Check Settings
    if str(int(settings["PORT"])) not in ('80', '6667', '443', '6697'):  # Convert into non-float string
        stopBot("Wrong Port! The port must be 80 or 6667 for standard connections, or 443 or 6697 for SSL")
    if not settings['BOT OAUTH']:
        stopBot("Missing BOT OAUTH - Please follow directions in the settings or readme.")
    if not ('oauth:' in settings['BOT OAUTH']):
        stopBot("Invalid BOT OAUTH - Your oauth should start with 'oauth:'")
    if not settings['BOT NAME'] or not settings['CHANNEL']:
        stopBot("Missing BOT NAME or CHANNEL - Please follow directions in the settings or readme")
    if settings["COMMAND PHRASE"]:
        if not "%cmd%" in settings["COMMAND PHRASE"]:
            stopBot("Your COMMAND PHRASE does not have %cmd% in it anywhere.")
        if len(settings["COMMAND PHRASE"].split("%cmd%", 1)[0]) < 3:
            stopBot("Your setting for COMMAND PHRASE is too short. You need at least 4 characters before %cmd%. ")
        print("\n\n IMPORTANT! You have a COMMAND PHRASE set in your Settings. NORMAL COMMANDS WON'T WORK!"
              "\n The bot will ONLY run commands via phrases sent only by the specified bot accounts. "
              "\n If you don't know what this means, remove your COMMAND PHRASE setting and read the documentation.\n")
        time.sleep(2)


    print(">> Initial Checkup Complete! Connecting to Chat...")
    return settings


def openSocket():
    global settings
    global s
    s = socket.socket()
    s.connect(("irc.chat.twitch.tv", int(settings["PORT"])))
    s.send(("PASS " + settings["BOT OAUTH"] + "\r\n").encode("utf-8"))
    s.send(("NICK " + settings["BOT NAME"] + "\r\n").encode("utf-8"))
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


if GenSettings:
    if not os.path.exists('../Config'):
        os.mkdir("../Config")

    if not os.path.exists('../Config/Settings.xlsx'):
        initSetup()
        print("\nPlease open Config / Settings.xlsx and configure the bot, then run it again.")
        print("Please read the readme to get everything set up!")
        time.sleep(3)
        quit()
    else:
        print("Everything is already set up!")

