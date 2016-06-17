
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#k::
Run http://ken.applnk.com:2305/print/kenken
WinMaximize KenKen(R)
WinWaitActive KenKen(R)
Click 555,569
WinWaitActive KenKen(R)
#s::
msgbox hi there
return
exit

Send ^p
return
WinWaitActive Print
Send {Enter}{Backspace}
return
WinWaitActive KenKen(R)
Click 329,569
WinWaitActive KenKen(R)
Send ^p {Enter} {Backspace}
return
WinWaitActive KenKen(R)
Click 111,569
WinWaitActive KenKen(R)
Send ^p{Enter}{Backspace}
WinWaitActive KenKen(R)
Click 555,362
WinWaitActive KenKen(R)
Send ^p{Enter}{Backspace}
WinWaitActive KenKen(R)
Click 123,362
WinWaitActive KenKen(R)
Send ^p{Enter}{Backspace}
return
