from Interact import *
from threading import Thread
from win32gui import GetWindowText, GetForegroundWindow


# TODO - REWORK THIS. Split the phrase to a left and right str, check if left is in cmd and right is in cmd, and if so remove both and you're left with the cmd.
class cmdPhrase:  # Anticommands, my name for grabbing the command from a chat message rather than a command.
    def __init__(self):
        self.fromLeft = 0
        self.fromRight = 0
        self.leftStr = ""
        self.rightStr = ""

    def trimSetting(self):
        if settings["COMMAND PHRASE"]:
            phrase = settings["COMMAND PHRASE"].lower()
            phrase = phrase.replace("%CMD%", "%cmd%")
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

        return toreturn.replace(settings["PREFIX"], '')


def formatted_time():
    return datetime.datetime.today().now().strftime("%I:%M")







class commands:
    def __init__(self):
        self.cooldowns = {}
        self.loadedGameCommands = []
        self.globalCommands = importGlobal()
        self.activeGame = None

    def runcommand(self, command, cmdArguments, user):
        run = False

        for item in self.loadedGameCommands, self.globalCommands:
            for i in item:
                if command.lower() == i[0].lower():
                    run = True


        if not run:
            chatConnection.sendToChat("Invalid command")

        if run:
            # Manage cooldowns
            if self.globalCooldown() > self.cmdCooldown(command):
                chatConnection.sendToChat("Since a command was run recently, nobody can interact for %s more seconds." % self.globalCooldown())
                return
            elif self.cmdCooldown(command) > self.globalCooldown():
                chatConnection.sendToChat("That command is still on cooldown for %s seconds." % self.cmdCooldown(command))
                return

            for item in cmd.loadedGameCommands:  # Test if the command run is for a loaded game
                if command.lower() == item[0].lower():  # Command detected, pass this to the InteractGame class.
                    cmdToRun = item[2]
                    cooldown = item[1]
                    if "%ARGS" in cmdToRun and not cmdArguments:
                        chatConnection.sendToChat("That command requires you to provide an argument to run.")
                        return
                    cmdToRun = cmdToRun.replace("%ARGS%", cmdArguments)
                    cmdToRun = cmdToRun.replace("%USER%", user)
                    self.runCmdExtras(command, cmdArguments, item)
                    interact(cmd.activeGame, cmdToRun, cooldown, cmdArguments, user)
                    return

            for item in self.globalCommands:  # Test if command run is a global command
                subOnly = item[4]
                donoReq = item[5]
                reward = item[6]
                if command.lower() == item[0].lower():  # Command detected, run the file

                    # RUN PRE-COMMAND CHECKS to make sure the user can actually run it
                    if subOnly:
                        if not mainChatConnection.isSubscriber:
                            chatConnection.sendToChat("This command can only be run by subscribers.")
                            return

                    if donoReq:
                        if not mainChatConnection.bitsAmount > donoReq:
                            chatConnection.sendToChat("This command can only be run with a donation of at least " + str(donoReq))
                            return


                    if item[2][0] == "$":  # Process built-in global script
                        if isValidInt(cmdArguments):  # Process MAX ARG setting
                            if int(cmdArguments) >= settings["MAX ARG"]:
                                chatConnection.sendToChat("That value is too high, please try again with a lower number.")
                                return

                        if not processBuiltInGlobal(item[2], cmdArguments, user):  # This runs the exe
                            chatConnection.sendToChat("That command requires you to provide an argument to run.")
                            return

                        self.runCmdExtras(command, cmdArguments, item)
                        return

                    if item[3]:  # Do this stuff if there's a specified active window
                        if item[3] in GetWindowText(GetForegroundWindow()):
                            self.runCmdExtras(command, cmdArguments, item)
                            script.runAHK(r"..\Config\UserScripts\\" + item[2])
                            return

                    else:  # Otherwise just active the command
                        self.runCmdExtras(command, cmdArguments, item)
                        script.runAHK(r"..\Config\UserScripts\\" + item[2])
                        return


    def globalCooldown(self):
        if "00rx_globalCD" in self.cooldowns.keys():  # This is just weird so theres no way anyone will ever accidentally have their command say this. Note, if your command says this and you ask for help, ill be pissed.
            timeleft = self.cooldowns["00rx_globalCD"] - datetime.datetime.now()
            return round(timeleft.total_seconds())
        return 0


    def cmdCooldown(self, command):
        if command in self.cooldowns.keys():
            timeleft = self.cooldowns[command] - datetime.datetime.now()
            return round(timeleft.total_seconds())
        return 0

    def runCmdExtras(self, command, cmdarguments, item):
        self.cooldowns.update({command: datetime.datetime.now() + datetime.timedelta(seconds=item[1])})
        self.cooldowns.update({"00rx_globalCD": datetime.datetime.now() + datetime.timedelta(seconds=settings["CD BETWEEN CMDS"])})
        writeArgs(cmdarguments)
        print(item[0] + " executed!")


class mainChat:
    def __init__(self):
        global settings
        self.channel = None
        self.bitsAmount = 0
        self.rewardTitle = None
        self.rewardCost = None
        self.isSubscriber = False
        self.cmdPhraseUsers = settings["ALT BOT NAMES"].replace(" ", "").lower().split(",")


    def main(self):
        chatConnection.start()
        while True:
            prefix = settings["PREFIX"]
            result = chatConnection.ws.recv()
            resultDict = json.loads(result)
            #print(resultDict)
            if debugMode:
                print(resultDict)
            if "event" in resultDict.keys() and not chatConnection.active:
                if "is_live" in resultDict["event"]:
                    print(">> Connection to chat successful!")
                    chatConnection.active = True
                    if chatConnection.puppet:
                        chatConnection.puppetlogin()

            if "event" in resultDict.keys():  # Any actual event is under this
                eventKeys = resultDict["event"].keys()

                # Update self.channel
                if "event_type" in eventKeys:
                    if resultDict['event']["event_type"] == "USER_UPDATE":
                        self.channel = resultDict['event']['streamer']['username']
                        if self.channel not in self.cmdPhraseUsers:
                            self.cmdPhraseUsers.append(self.channel)

                if "reward" in eventKeys:
                    self.rewardTitle = resultDict["event"]["reward"]["title"]
                    rewardPrompt = resultDict["event"]["reward"]["prompt"]
                    self.rewardCost = resultDict["event"]["reward"]["cost"]
                    user = resultDict["event"]["sender"]["displayname"]
                    print(
                        "(" + misc.formatTime() + ")>> [EVENT] " + user + " redeemed reward title %s, prompt %s, for %s points." % (self.rewardTitle, rewardPrompt, self.rewardCost))

                if "subscriber" in eventKeys:
                    try:
                        subUsername = resultDict["event"]["subscriber"]["username"]
                        subMonths = resultDict["event"]["months"]
                        subLevel = resultDict["event"]["sub_level"]
                        print(
                            "(" + misc.formatTime() + ")>> [EVENT] " + subUsername + " subscribed with level %s for %s months." % (subLevel, subMonths))
                        self.isSubscriber = True
                    except:
                        pass

                if "donations" in eventKeys:
                    if resultDict["event"]["donations"]:
                        self.bitsAmount = round(resultDict["event"]["donations"][0]["amount"])
                        user = resultDict["event"]["sender"]["displayname"]
                        message = resultDict["event"]["message"]
                        print("(" + misc.formatTime() + ")>> [EVENT] " + user + " cheered %s bits with the message %s" % (self.bitsAmount, message))


                if "message" in eventKeys:  # Got chat message, display it then process commands
                    try:
                        message = resultDict["event"]["message"]
                        if message:
                            user = resultDict["event"]["sender"]["displayname"]
                            command = ((message.split(' ', 1)[0]).lower()).replace("\r", "")
                            cmdarguments = message.replace(command or "\r" or "\n", "")[1:]
                            if "SUBSCRIBER" in resultDict["event"]["sender"]["roles"]:
                                self.isSubscriber = True
                            else:
                                self.isSubscriber = False
                            print("(" + misc.formatTime() + ")>> " + user + ": " + message)


                            if settings["COMMAND PHRASE"]:  # Process anticommands
                                if user.lower() in self.cmdPhraseUsers:
                                    if commandPhrase.trimSetting() in message.lower():
                                        extractedCmd = commandPhrase.extractCmd(message)
                                        cmdarguments = (extractedCmd.replace(extractedCmd.split(" ")[0], '')).strip()
                                        toRun = extractedCmd.split(" ")[0]
                                        print("Running command from another bot: " + toRun)
                                        cmd.runcommand(prefix + toRun, cmdarguments, user)

                            elif command[0] == prefix:  # Only run normal commands if COMMAND PHRASE is blank
                                cmd.runcommand(command, cmdarguments, user)

                            self.bitsAmount = 0

                    except PermissionError:
                        pass

            if "disclaimer" in resultDict.keys():  # Should just be keepalives?
                if resultDict["type"] == "KEEP_ALIVE":
                    response = {"type": "KEEP_ALIVE"}
                    chatConnection.sendRequest(response)

            if "error" in resultDict.keys():
                print("CHAT CONNECTION ERROR : " + resultDict["error"])
                if resultDict['error'] == "USER_AUTH_INVALID":
                    print("Channel Auth Token Expired or Invalid - Reauthenticating...")
                    authenticate()
                elif resultDict['error'] == "PUPPET_AUTH_INVALID":
                    print("Bot Account Auth Token Expired or Invalid -  Reauthenticating...")
                    authenticate()
                else:
                    print("Please report this error to rxbots so we can get it resolved.")
                    print("Try running RXBOT_DEBUG.bat in the RxBot folder to get more info on this error to send to me.")


supportedGames = {
    # Window Name : Function Name
    "Skyrim Special Edition": "Skyrim",
    "Oblivion": "Oblivion",
    "Fallout4": "Fallout 4",
    "Fallout: New Vegas": "Fallout NV",
    "Fallout3": "Fallout 3",
    "Minecraft": "Minecraft",
    "Subnautica": "Subnautica",
    "Subnautica Below Zero": "Subnautica",
    "The Witcher 3": "Witcher 3",
    "Valheim": "Valheim"
}


def refresh():
    cacheActiveGame = ''
    cmd.activeGame = None
    while True:
        time.sleep(2)
        currentWindow = GetWindowText(GetForegroundWindow())

        cmd.activeGame = None

        for winName in supportedGames:
            if winName in currentWindow and (cmd.activeGame != supportedGames[winName]):
                cmd.activeGame = supportedGames[winName]

        if cacheActiveGame != cmd.activeGame and cmd.activeGame:  # Do when user starts NEW game
            print("Now playing " + cmd.activeGame)
            cacheActiveGame = cmd.activeGame
            if settings['ANNOUNCE GAME']:
                chatConnection.sendToChat("The streamer is now playing " + cmd.activeGame + " and you can interact with it!")
            cmd.loadedGameCommands = importInteraction(cmd.activeGame)

        elif not cmd.activeGame:  # If no game is loaded
            cmd.loadedGameCommands = []

        elif cmd.activeGame and (len(cmd.loadedGameCommands) == 0):  # If the game is tabbed back in, but not a new game (don't announce it)
            cmd.loadedGameCommands = importInteraction(cmd.activeGame)


def tick():
    while True:  # Test for cooldowns being complete
        time.sleep(0.5)
        if cmd.cooldowns:
            for item in cmd.cooldowns:
                if cmd.cooldowns[item] <= datetime.datetime.now():
                    cmd.cooldowns.pop(item)
                    break


mainChatConnection = mainChat()
commandPhrase = cmdPhrase()
cmd = commands()

t1 = Thread(target=mainChatConnection.main)
t2 = Thread(target=refresh)
t3 = Thread(target=tick)

t1.start()
t2.start()
t3.start()

