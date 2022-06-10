#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force
SetKeyDelay,80,20
SendMode, input
Blockinput, On

KeyList := "Shift|w|a|s|d|e|f|r|Space"

Loop, Parse, KeyList, |
{
    Send % "{" A_Loopfield " Up}"
}

Sleep, 60
SendInput, {`` Down}
Sleep, 60
SendInput, {`` up}
Sleep, 60


SendInput, {Enter Down}
Sleep, 60
SendInput, {Enter up}
Sleep, 60


Loop, read, cmd.txt
{
    Loop, parse, A_LoopReadLine, %A_Tab%
    {
        SendInput, {%A_LoopField% down}
		Sleep, 22
		SendInput, {%A_LoopField% up}
		Sleep, 22
    }
}

Sleep, 60
SendInput, {Enter Down}
Sleep, 60
SendInput, {Enter up}
Sleep, 60

SendInput, {`` Down}
Sleep, 60
SendInput, {`` up}
Sleep, 60

return