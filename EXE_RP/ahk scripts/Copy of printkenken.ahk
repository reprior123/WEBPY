
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#space::
Run http://www.kenken.com/
WinMaximize Welcome to KENKEN
Return
click 488,475
click 909,644
WinMaximize KenKen
click 341,345
Return
Send ^p {Enter} {Backspace}
Return
Click 577,362
Click 123,414
Click 111,569
Click 329,569
Click 555,569


