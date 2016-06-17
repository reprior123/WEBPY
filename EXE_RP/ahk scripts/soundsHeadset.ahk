;


#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

Run C:\Documents and Settings\bob marley\Desktop\ShortcutSound.lnk
WinActivate Sounds and Audio
WinWaitActive Sounds and Audio
;Send ^{tab} ^{tab}A{Enter}
return

#H::
Run C:\Documents and Settings\bob marley\Desktop\ShortcutSound.lnk
WinActivate Sounds and Audio
WinWaitActive Sounds and Audio
;Send ^{tab} ^{tab}A{Enter}
return
