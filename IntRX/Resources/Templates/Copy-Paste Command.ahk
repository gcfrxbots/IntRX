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

; If you have anything currently copied to your clipbaord, this backs it up.
SavedClip := ClipboardAll

; Copies the command to your clipboard. Change "Something" to your command (keep the quotes).
Clipboard := "Something"

; Pastes your command.
Send ^v

; Copies what was backed up earlier.
Clipboard := SavedClip
SavedClip := ""

; Types whatever key sends the command, usually Enter.
SendInput, {Enter Down}
Sleep, 15
SendInput, {Enter up}
Sleep, 15

; Closes the script.
return