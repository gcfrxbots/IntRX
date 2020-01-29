#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance force

; If you often use a certain key in the game you play, add that key to this list with the | separating it.
KeyList := "Shift|w|a|s|d|e|f|r|Space"
Loop, Parse, KeyList, |
{
    Send % "{" A_Loopfield " Up}"
}

; Add OBS.txt as a text source in OBS to have it show on your stream.
FileAppend, Charge, OBS.txt
SetKeyDelay,80,40
Blockinput, On

; Holds W, and clicks every 250ms. Change Sleep from 250 to make the delay longer or shorter.
; Loop is how many times the script clicks before it ends, default 40 times. Change it if you wish.
Send, {W down}
Loop, 40
{
Click
Sleep, 250
}
Send, {W up}

FileDelete, OBS.txt