; For a more in-depth explanation on these templates, visit https://rxbots.net/intrx-creating-your-own-scripts.html

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force
SetKeyDelay,40,20
SendMode, input
Blockinput, On

; Do NOT touch anything above this line unless you know what you're doing. This stuff is to stop any keys you're pressing from interfering with the script, and to ensure it works with your game.


FileRead, CommandVar, ..\..\Config\UserScripts\output.txt

Input = %CommandVar%


SendInput, {%Input% down}
Sleep, 70
SendInput, {%Input% up}
Sleep, 45

	
