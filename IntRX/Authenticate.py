import string
import random
import webbrowser
import os
from Initialize import *

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def formatted_time():
    return datetime.datetime.today().now().strftime("%I:%M")


def ran16characterstring():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(16))

def ran8digitstring():
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(8))

def message(msg):
    cls()
    print("\n\n\n\n\n\n>>>>>---------------------------------------------------------------------------<<<<<")
    print(msg)
    print(">>>>>----------------------------------------------------------------------------<<<<<")
    time.sleep(3)
    cls()


validPlatforms = ["twitch", "youtube", "trovo", "glimesh", "brime", "caffeine"]

def getPlatform():
    if not os.path.exists('../Config/Settings.xlsx'):
        path = os.path.abspath("../Setup/Install_Requirements.bat")
        subprocess.call(path)
        return
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
                        print("Platform %s is invalid! Please change the PLATFORM setting to a valid supported platform." % setting)
                        quit()

                else:
                    print("No platform detected.")




class chatAuth:
    def __init__(self):
        self.rndString = ran16characterstring()
        self.authLine = "auth_redirect%3A{rndstring}%3Acaffeinated_{platform}%3AjJu2vQGnHf5U5trv".format(rndstring=self.rndString, platform=getPlatform())
        self.url = "wss://api.casterlabs.co/v1/kinoko?type=parent&channel=" + self.authLine

        self.ws = create_connection(self.url)

    def sendRequest(self, request):
        self.ws.send(request)

    def main(self, account):
        if account == "main":
            print("Please open the browser window and sign in to your CHANNEL's account.")
        else:
            print("Please open the browser window and sign in to your BOT's account.")
        time.sleep(2)
        webbrowser.open("https://casterlabs.co/auth/redirect/?state=" + self.authLine)
        while True:
            time.sleep(0.2)
            result = self.ws.recv()

            if ":ping" in result:
                self.sendRequest(":ping")


            if "token:" in result and account == "main":
                token = json.loads(result)
                token = token.split(":")[1]

                path = os.path.abspath("../Config/tokens/token_{platform}.txt".format(platform=getPlatform()))
                with open(path, "w") as file:
                    file.write(token)
                    file.close()

                    cls()
                    print("Login to your channel's account successful!\n\n")
                    time.sleep(2)
                    print("Do you wish to have the bot chat through a different user? If you choose No, your bot will send messages to chat from your own account, not its own bot account.")
                    inp = input("Please type Y or N\n >> ").lower()

                    if inp == "n":
                        changeChatSetting(False)
                        return
                    else:
                        print("The bot can send all chat messages as the user rxbots, or as your own second account. Please type the number of your choice and press Enter:")
                        print("1. Send all chat messages as the user rxbots")
                        print("2. Send all chat messages as a different user  [ Warning - Will require a subscription to Casterlabs Plus in the future ]")
                        inp = input("Please type 1 or 2\n >> ")
                        while inp not in ['1', '2']:
                            inp = input("Please type 1 or 2\n >> ")  # TODO - Might be freezing here
                        if inp == '1':
                            changeChatSetting(True)
                        elif inp == '2':
                            changeChatSetting(False)
                            self.main("puppet")

                        print("Login successful! All set, you can close this now.")

            if "token:" in result and account == "puppet":
                token = json.loads(result)
                token = token.split(":")[1]
                with open("../Config/tokens/puppet_{platform}.txt".format(platform=getPlatform()), "w") as file:
                    file.write(token)
                    file.close()
                    print("Login to your bot's account successful! All set, you can close this now.")
                    return


class CaffeinatedChatAuth:
    def __init__(self):
        self.rndCode = ran8digitstring()
        self.url = "wss://api.casterlabs.co/v1/kinoko?type=parent&channel=casterlabs_pairing%3A" + self.rndCode

        self.ws = create_connection(self.url)

    def sendRequest(self, request):
        self.ws.send(request)

    def main(self, account):
        print("Please follow these steps to authenticate with Caffeine:")

        if account == "main":
            print('''1. Open Caffeinated (Download from casterlabs.co)
            2. Select Settings from the menu on the left sidebar
            3. Select "Streaming Services" under Accounts on the left sidebar
            4. Select Caffeine and sign into your Caffeine account.
            5. Once you're signed in, select "Pair a Device" under Accounts on the left sidebar
            6. Enter the following code: %s''' % self.rndCode)


        while True:
            time.sleep(0.2)
            result = self.ws.recv()

            if ":ping" in result:
                self.sendRequest(":ping")

            if "what" in result:
                self.sendRequest("what:IntRX:PLATFORM_AUTH")


            if "token:" in result and account == "main":
                token = result.split(":")[1]
                path = os.path.abspath("../Config/tokens/token_{platform}.txt".format(platform=getPlatform()))
                with open(path, "w") as file:
                    file.write(token)
                    file.close()


                    print("Login to your channel's Twitch account successful!\n\n")
                    print("Do you wish to have the bot chat as the user Rxbots? If you choose No, your bot will send messages to chat from your own account.")
                    inp = input("Please type Y or N\n >> ").lower()

                    if inp == "n":
                        changeChatSetting(False)
                        return
                    else:
                        changeChatSetting(True)
                        return

authChatConnection = chatAuth()
CaffeinatedAuthChatConnection = CaffeinatedChatAuth()

if __name__ == "__main__":
    if getPlatform() == "caffeine":
        CaffeinatedAuthChatConnection.main("main")
    else:
        authChatConnection.main("main")

