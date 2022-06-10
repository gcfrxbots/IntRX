import os
import argparse
import time
import shutil
import json
from websocket import create_connection
import urllib, urllib.request
import subprocess
import datetime
from distutils.dir_util import copy_tree

try:
    import xlrd
    import xlsxwriter
    from openpyxl import load_workbook
except ImportError as e:
    print(e)
    raise ImportError(">>> One or more required packages are not properly installed! Run INSTALL_REQUIREMENTS.bat to fix!")


parser = argparse.ArgumentParser(description='Generate Settings File')
parser.add_argument('--g', dest="GenSettings", action="store_true")
parser.add_argument('--d', dest="debugMode", action="store_true")
parser.set_defaults(GenSettings=False, debugMode=False)

GenSettings = (vars(parser.parse_args())["GenSettings"])
debugMode = (vars(parser.parse_args())["debugMode"])

'''----------------------SETTINGS----------------------'''

'''FORMAT ---->   ("Option", "Default", "This is a description"), '''
defaultSettings = [
    ("PLATFORM", "Twitch", "Choose your streaming platform: Twitch, Youtube, Caffeine, Brime, Trovo, Glimesh."),
    ("CHAT AS RXBOTS", "No", "Set to Yes for all bot messages in your chat to be sent from the user rxbots, or No if you want the messages to be from your own account or your own bot account."),
    ("", "", ""),
    ("ANNOUNCE GAME", "Yes", "Announce in chat when you begin playing a game that the bot supports. (Yes/No)"),
    ("REFRESH INTERVAL", 5, "The period of time, in seconds, that the bot refreshes your active window to load or unload commands for a game."),
    ("CD BETWEEN CMDS", 15, "The cooldown, in seconds, between two consecutive commands."),
    ("MAX ARG", 25, "The highest integer that a user can provide for %ARGS%. Used to prevent things like $SPAM from being run 99999 times."),
    ("", "", ""),
    ("ALT BOT NAME", "", "If you use another bot which uses its own Twitch account, such as NightBot or StreamElements, type its name here (Lowercase)"),
    ("COMMAND PHRASE", "", "If this isn't empty, commands will only be accepted from your bot(s), and must be executed via this phrase. Use %cmd% to mark where the command goes. Check the site for more info."),
]
'''----------------------END SETTINGS----------------------'''

# TODO - ADD "USE PREFIX" SETTING - See most recent post in #scripts
# TODO - Make CHAT AS RXBOTS work - See message from END3R
# TODO - Finish Interactconfig changes
# TODO - NEW COMMAND PHRASES


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
            worksheet.set_column(2, 2, 180)
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
            listGames = ("Skyrim", "Oblivion", "Fallout 4", "Fallout NV", "Fallout 3", "Minecraft", "Subnautica", "Witcher 3", "Valheim")

            format = workbook.add_format({'bold': True, 'center_across': True, 'font_color': 'white', 'bg_color': 'gray'})
            lightformat = workbook.add_format({'center_across': True, 'font_color': 'black', 'bg_color': '#DCDCDC', 'border': True})
            evenlighterformat =  workbook.add_format({'center_across': True, 'font_color': 'black', 'bg_color': '#f0f0f0', 'border': True})
            redformat = workbook.add_format({'font_color': 'black', 'bg_color': '#ffdede', 'border': True})
            greenformat = workbook.add_format({'font_color': 'black', 'bg_color': '#e6ffd4', 'border': True})

            worksheet = workbook.add_worksheet("Global")  # FORMAT GLOBAL
            worksheet.set_column(0, 0, 30)
            worksheet.set_column(1, 1, 10)
            worksheet.set_column(2, 2, 10)
            worksheet.set_column(3, 3, 45)
            worksheet.set_column(4, 4, 100)
            worksheet.set_column(5, 5, 20)
            worksheet.write(0, 0, "Command", format)
            worksheet.write(0, 1, "Cooldown", format)
            worksheet.write(0, 2, "Disable", format)
            worksheet.write(0, 3, "Active Window", format)
            worksheet.write(0, 4, "What to Run", format)
            worksheet.write(0, 5, "Sub Only", format)
            worksheet.write(0, 6, "Donation Cost", format)
            worksheet.write(0, 7, "Reward to Redeem", format)
            worksheet.set_column('B:B', 10, lightformat)
            worksheet.set_column('C:C', 10, redformat)
            worksheet.set_column('D:D', 30, evenlighterformat)
            worksheet.set_column('F:H', 20, greenformat)

            for item in listGames:  # FORMAT GAMES
                worksheet = workbook.add_worksheet(item)
                worksheet.set_column(0, 0, 30)
                worksheet.set_column(1, 1, 10)
                worksheet.set_column(2, 2, 10)
                worksheet.set_column(3, 3, 110)
                worksheet.set_column(4, 4, 20)
                worksheet.write(0, 0, "Command", format)
                worksheet.write(0, 1, "Cooldown", format)
                worksheet.write(0, 2, "Disable", format)
                worksheet.write(0, 3, "Command To Execute", format)
                worksheet.write(0, 4, "Sub Only", format)
                worksheet.write(0, 5, "Donation Cost", format)
                worksheet.write(0, 6, "Reward to Redeem", format)
                worksheet.set_column('B:B', 10, lightformat)  # END FORMATTING
                worksheet.set_column('C:C', 10, redformat)  # END FORMATTING
                worksheet.set_column('E:G', 20, greenformat)
            # Create Global Worksheet

        print("InteractConfig.xlsx has been updated successfully.")
    except PermissionError:
        stopBot("Can't open the InteractConfig file. Please close it and make sure it's not set to Read Only")


def readSettings():
    wb = xlrd.open_workbook('../Config/Settings.xlsx')
    sheet = wb.sheet_by_name("Settings")
    for item in range(sheet.nrows):
        if item == 0:
            pass
        else:
            option = sheet.cell_value(item,0)
            setting = sheet.cell_value(item,1)
            if setting == "Yes":
                setting = True
            if setting == "No":
                setting = False

            settings[option] = setting

    # Check for new/changed settings
    if sheet.nrows != (len(defaultSettings)+1):
        for item in settings:
            for i in enumerate(defaultSettings):
                if (i[1][0]) == item:
                    defaultSettings[i[0]] = (item, settings[item], defaultSettings[i[0]][2])
        formatSettingsXlsx()
        stopBot("The settings for IntRX have changed since you last started the script. Settings.xlsx has updated, go check it out.")

    return settings


def changeChatSetting(setting):  # An overcomplicated function that exists only to allow users to be lazy and not have to change the CHAT AS RXBOTS setting themselves.
    try:
        workbook = load_workbook('../Config/Settings.xlsx')
        ws = workbook["Settings"]
        cellToEdit = None

        for settingEntry in enumerate(defaultSettings):
            row = settingEntry[0] + 2
            if settingEntry[1][0] == "CHAT AS RXBOTS":
                cellToEdit = "B" + str(row)

        if setting:
            ws[cellToEdit] = "Yes"
        else:
            ws[cellToEdit] = "No"

        workbook.save('../Config/Settings.xlsx')

    except PermissionError:
        stopBot("Can't read/edit Settings.xlsx! Please close it and make sure it isn't read only!")




def getPlatform():
    validPlatforms = ["twitch", "youtube", "trovo", "glimesh", "brime", "caffeine"]
    wb = xlrd.open_workbook('../Config/Settings.xlsx')
    sheet = wb.sheet_by_name("Settings")
    for item in range(sheet.nrows):
        if item == 0:
            pass
        else:
            option = sheet.cell_value(item,0)
            setting = sheet.cell_value(item,1)
            if option == "PLATFORM":
                if setting:
                    if setting.lower() in validPlatforms:
                        return setting.strip().lower()
                    else:
                        print("Platform %s is invalid! Please change the PLATFORM setting to a valid supported platform." % setting )
                else:
                    print("No platform detected.")


def authenticate():
    path = os.path.abspath("../Setup/Authenticate.bat")
    subprocess.call(path)


def initSetup():
    global settings
    settings = {}
    killbot = False
    if not os.path.exists('../Config'):
        os.mkdir("../Config")

    if not os.path.exists('../Config/tokens'):
        os.mkdir("../Config/tokens")

    if not os.path.exists('../Config/UserScripts'):
        os.mkdir("../Config/UserScripts")

        for file in os.listdir("./Resources/Included Scripts"):
            full_file_name = os.path.join("./Resources/Included Scripts", file)
            if os.path.isfile(full_file_name) and (".ahk" not in full_file_name):
                shutil.copy(full_file_name, "../Config/UserScripts")


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
    settings = readSettings()

    if settings["COMMAND PHRASE"]:
        settingsCmdPhrase = settings["COMMAND PHRASE"].replace("%CMD%", "%cmd%")
        if not "%cmd%" in settingsCmdPhrase:
            stopBot("Your COMMAND PHRASE does not have %CMD% in it anywhere.")
        if len(settingsCmdPhrase.split("%cmd%", 1)[0]) < 3:
            stopBot("Your setting for COMMAND PHRASE is too short. You need at least 4 characters before %CMD%. ")
        print("\n\n IMPORTANT! You have a COMMAND PHRASE set in your Settings. NORMAL COMMANDS WON'T WORK!"
              "\n The bot will ONLY run commands via phrases sent only by the specified bot accounts. "
              "\n If you don't know what this means, remove your COMMAND PHRASE setting and read the documentation.\n")
        time.sleep(2)

    # Set the normal token
    platform = getPlatform()

    if os.path.exists("../Config/tokens/token_{platform}.txt".format(platform=platform)):
        with open("../Config/tokens/token_{platform}.txt".format(platform=platform), "r") as f:
            chatConnection.token = f.read()
            f.close()
    else:
        print("Casterlabs authentication needed...")
        time.sleep(1)
        # Run authenticate separately to avoid import loops
        authenticate()

        time.sleep(1)
        with open("../Config/tokens/token_{platform}.txt".format(platform=platform), "r") as f:
            chatConnection.token = f.read()
            f.close()

    # Set the puppet token, if it exists
    if os.path.exists("../Config/tokens/puppet_{platform}.txt".format(platform=platform)):
        chatConnection.puppet = True
        with open("../Config/tokens/puppet_{platform}.txt".format(platform=platform), "r") as f:
            chatConnection.puppetToken = f.read()
            f.close()


    # Read settings again after them potentially being changed
    settings = readSettings()

    print(">> Initial checkup complete!")
    return settings


class chat:
    global settings

    def __init__(self):
        self.ws = None
        self.url = "wss://api.casterlabs.co/v2/koi?client_id=jJu2vQGnHf5U5trv"
        self.caffeineUrl = "wss://api.casterlabs.co/v2/koi?client_id=LmHG2ux992BxqQ7w9RJrfhkW"
        self.puppet = False
        self.active = False
        self.token = None
        self.puppetToken = None

    def login(self):
        loginRequest = {
                "type": "LOGIN",
                "token": self.token
            }
        self.ws.send(json.dumps(loginRequest))
        time.sleep(1)

    def puppetlogin(self):
        time.sleep(1.5)
        loginRequest = {
            "type": "PUPPET_LOGIN",
            "token": self.puppetToken
        }
        self.ws.send(json.dumps(loginRequest))

    def sendRequest(self, request):
        self.ws.send(json.dumps(request))

    def sendToChat(self, message):
        if message:
            if not self.puppet:
                    request = {
                      "type": "CHAT",
                      "message": message,
                      "chatter": "CLIENT"}
            else:
                request = {
                    "type": "CHAT",
                    "message": message,
                    "chatter": "PUPPET"}
            self.sendRequest(request)

    def start(self):
        if getPlatform() == "caffeine":
            self.ws = create_connection(self.caffeineUrl)
        else:
            self.ws = create_connection(self.url)
        self.login()
        print(">> Connecting to platform: " + getPlatform().capitalize())


class runMiscControls:

    def __init__(self):
        self.timerActive = False
        self.timers = {}

    def getUser(self, line):
        seperate = line.split(":", 2)
        user = seperate[1].split("!", 1)[0]
        return user

    def getMessage(self, line):
        seperate = line.split(":", 2)
        message = seperate[2]
        return message

    def formatTime(self):
        return datetime.datetime.today().now().strftime("%I:%M")

    def setTimer(self, name, duration):
        self.timerActive = True
        curTime = datetime.datetime.now()
        targetTime = curTime + datetime.timedelta(seconds=duration)
        self.timers[name] = targetTime

    def timerDone(self, timer):
        self.timers.pop(timer)
        print(timer + " timer complete.")
        if not self.timers:
            self.timerActive = False


misc = runMiscControls()
chatConnection = chat()


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

