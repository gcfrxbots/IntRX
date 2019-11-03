#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force
SetKeyDelay,40,20
SendMode, input
Blockinput, On

KeyList := "Shift|w|a|s|d|e|f|r|Space"

Loop, Parse, KeyList, |
{
    Send % "{" A_Loopfield " Up}"
}

; Do NOT touch anything above this line unless you know what you're doing. This stuff is to stop any keys you're pressing from interfering with the script, and to ensure it works with your game.



; Type something to open up the game's console, if necessary

SendInput, {`` Down}
Sleep, 15
SendInput, {`` up}
Sleep, 15

; Send your input to the game. This can be done a varitey of ways, and depends heavily on the game. Use "Send" for the easiest input.
; I have found that using SendInput for individual keys, with a 15 to 30ms delay between pressing and releasing, is the most univerally functional method.

; This loop should be FAIRLY universal in sending input to a game. It might need to be changed depending on the game. Play with the delays.

Input = Something

Loop, Parse, Input
{
	SendInput, {%A_LoopField% down}
	Sleep, 25
	SendInput, {%A_LoopField% up}
	Sleep, 25
}



; Do whatever is needed to send the command, then close the console.

SendInput, {Enter Down}
Sleep, 15
SendInput, {Enter up}
Sleep, 15


SendInput, {`` Down}
Sleep, 15
SendInput, {`` up}
Sleep, 15

return