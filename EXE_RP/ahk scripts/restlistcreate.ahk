;
; AutoHotkey Version: 1.x
; Language:       English
; Platform:       Win9x/NT
; Author:         A.N.Other <myemail@nowhere.com>
;
; Script Function:
;	Template script (you can customize this template by editing "ShellNew\Template.ahk" in your Windows folder)
;

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#space::
;Run C:\Program Files\Microsoft Office\OFFICE11\Excel.exe
;IfWinExist Microsoft Excel - get.links.ppdbase.xls
;{
;    WinActivate
;}
;else
;{
;Run C:\Documents and Settings\bob marley\My Documents\get.links.ppdbase.rests.xls
;   Run Notepad
;    WinWait Microsoft Excel - get.links.ppdbase.xls
;    WinActivate
;}
;Return
;WinActivate InputBox Demo
;
Loop,100
{
Send ^s ^v {Enter} ^w
sleep 3000
WinWait InputBox Demo
WinActivate InputBox Demo
Send {Enter}
sleep 9000
}
return 
