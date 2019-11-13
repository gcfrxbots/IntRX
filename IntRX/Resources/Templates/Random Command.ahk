; For a more in-depth explanation on these templates, visit https://rxbots.net/intrx-creating-your-own-scripts.html

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force
SetKeyDelay,40,20
SendMode, input
Blockinput, On

; Do NOT touch anything above this line unless you know what you're doing. This stuff is to stop any keys you're pressing from interfering with the script, and to ensure it works with your game.

; If you often use a certain key in the game you play, add that key to this list with the | separating it.
KeyList := "Shift|w|a|s|d|e|f|r|Space"

; Releases any keys from the KeyList you currently have pressed, so it doesn't break the command.
Loop, Parse, KeyList, |
{
    Send % "{" A_Loopfield " Up}"
}

; Types something to open up the game's console. This section can be removed if not needed.
SendInput, {`` Down}
Sleep, 15
SendInput, {`` up}
Sleep, 15

; Write your commands here. Make as many as you want.
command1=First command
command2=Second command

; Selects a random command from the list above. Replace 2 with the number of commands listed.
; If you added more commands, every additional command will need a new else If and Input line.
Random, output, 1, 2
If output=1
Input = %command1%
else If output=2
Input = %command2%

; Sends your input to the game with what we've found to be the most universally functional method. Sleep is the delay, in milliseconds, between pressing the key and releasing it.
; Play around with the Sleep delay if you want. If you'd like to try to get the command to be input quicker, decrease it. If the command is being input too fast for your game to handle, increase it.
Loop, Parse, Input
{
	toPrint = %A_LoopField%
	if toPrint is space
	{
		toPrint = Space
	}
	SendInput, {%toPrint% down}
	Sleep, 25
	SendInput, {%toPrint% up}
	Sleep, 25
}

; Types whatever key sends the command, usually Enter.
SendInput, {Enter Down}
Sleep, 15
SendInput, {Enter up}
Sleep, 15

; Closes the console. Again, remove if not needed.
SendInput, {`` Down}
Sleep, 15
SendInput, {`` up}
Sleep, 15

; Closes the script.
return