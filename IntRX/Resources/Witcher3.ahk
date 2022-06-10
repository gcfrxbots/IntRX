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

SendInput, {F2 Down}
Sleep, 25
SendInput, {F2 up}
Sleep, 50


SendInput, {Enter Down}
Sleep, 25
SendInput, {Enter up}
Sleep, 25


Loop, read, cmd.txt
{
    Loop, parse, A_LoopReadLine, %A_Tab%
    {
		toPrint = %A_LoopField%
		if ("C" toPrint = "C(" or "C" toPrint = "C)" or "C" toPrint = "C_")
			{ 
			SendInput, {Shift Down}
			Sleep, 25
			SendInput, {%A_LoopField% down}
			Sleep, 25
			SendInput, {%A_LoopField% up}
			Sleep, 25
			SendInput, {Shift Up}
			Sleep, 25
			}
		else
			{
			SendInput, {%A_LoopField% down}
			Sleep, 25
			SendInput, {%A_LoopField% up}
			Sleep, 25
			}
    }
}

Sleep, 35
SendInput, {Enter Down}
Sleep, 35
SendInput, {Enter up}
Sleep, 40

SendInput, {F2 Down}
Sleep, 25
SendInput, {F2 up}
Sleep, 15

return