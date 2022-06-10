; For a more in-depth explanation on these templates, visit https://rxbots.net/intrx-creating-your-own-scripts.html

; This isn't an actual template, but you can paste these two sections of code into any script.
; This code will output some text to a .txt file while the script is active.
; You can add this code to any script you want.

; Creates OBS.txt and writes your text to it.
; Paste this line near the beginning of your script, such as before KeyList.
FileAppend, Your Text Here, OBS.txt

; Deletes OBS.txt.
; Paste this line after everything else in your script, right before return.
FileDelete, OBS.txt

; Change this from 0 if you want the text to stay a few seconds longer.
Sleep 0

; Closes the script.
return