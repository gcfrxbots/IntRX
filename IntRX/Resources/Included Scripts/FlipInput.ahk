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
FileAppend, FlipInput, OBS.txt

; 23600+1400=25000. That's how long the script lasts by default, in milliseconds.
; Change the number here to increase or decrease the length. Definitely change per-game.
SetTimer, Reverse,-23600
return

Reverse:
    FileDelete, OBS.txt
	sleep 1400
    ExitApp
Return

; Reverses your movement controls.
 w::s
 s::w
 a::d
 d::a
 
 ; Swaps Space and E for fun. You can change or remove these, or even add your own.
 Space::e
 e::Space