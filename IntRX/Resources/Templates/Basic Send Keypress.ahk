; For a more in-depth explanation on these templates, visit https://rxbots.net/intrx-creating-your-own-scripts.html

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#SingleInstance force
SetKeyDelay,40,20
SendMode, input
Blockinput, On

; Do NOT touch anything above this line unless you know what you're doing. This stuff is to stop any keys you're pressing from interfering with the script, and to ensure it works with your game.


;  |
;  |  This is all you need to change to just send one single keystroke! Simply change 's' to any key you want to press.
;  V  For non-digits, just type their name, ie Enter, Space, Up, End, etc.

Input = s


SendInput, {%Input% down}
Sleep, 45
SendInput, {%Input% up}
Sleep, 45
; If for some reason the key doesn't seem to be 'releasing' in the game, increase these delays a bit.
	
