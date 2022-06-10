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
FileAppend, Freeze, OBS.txt

; The sum of these two Sleeps is how long your input is blocked in milliseconds. Default ten seconds.
; Adjust the length of the script by changing the first Sleep, don't touch the second one.
BlockInput, On
sleep 8600
FileDelete, OBS.txt
sleep 1400