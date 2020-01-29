#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
#SingleInstance, force
SetKeyDelay,80,20

; Add OBS.txt as a text source in OBS to have it show on your stream.
FileAppend, TerribleAim, OBS.txt

; Moves the mouse eratically every 750ms. Change the Sleeps to increase or decrease the delay.
; By default, the mouse will move six times per loop. Change the number of loops if you wish.
; You may also have to change the first two MouseMove numbers, depending on the game.
; If the mouse moves too much, decrease the first two numbers. If it doesn't move enough, increase them.
Loop, 5
{
MouseMove, 50, -50 , 100, R
Sleep, 750
MouseMove, -100, 0 , 100, R 
Sleep, 750
MouseMove, 0, 100 , 100, R
Sleep, 750
MouseMove, 100, 0 , 100, R
Sleep, 750
MouseMove, 0, -100 , 100, R
Sleep, 750
MouseMove, -50, 50 , 100, R
Sleep, 750
}

FileDelete, OBS.txt
