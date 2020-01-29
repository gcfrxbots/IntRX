#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
SendMode Input
SetKeyDelay,80,40

; Reads what key the user typed after the command.
FileRead, KeyToSpam, output.txt

; Add OBS.txt as a text source in OBS to have it show on your stream.
FileAppend, SpamKey (%KeyToSpam%), OBS.txt

; A list of keys not allowed to be used with this command. Separate new items with commas, no spaces.
; Full key list here: https://www.autohotkey.com/docs/KeyList.htm
ForbiddenKeys := "LWin,RWin"

; Closes the script if the specified key is forbidden.
If KeyToSpam in %ForbiddenKeys%
ExitApp

; Don't touch, this is so users can't break or abuse the command.
else If KeyToSpam contains {,}
ExitApp

; Sends the letter once every 500ms. Change Sleep from 500 to make the delay longer or shorter.
; Loop is how many times the key is pressed before it ends, default 20 times. Change it if you wish.
else
Loop, 20
{
	Send, {%KeyToSpam% down}
	Sleep, 75
	Send, {%KeyToSpam% up} 
	Sleep, 500
}

FileDelete, OBS.txt