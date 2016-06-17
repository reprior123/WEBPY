#n::
; Write to the array:
ArrayCount = 0
run, notepad.exe
Loop, Read, C:\TS\stocklist.txt   ; This loop retrieves each line from the file, one at a time.
{
    ArrayCount += 1  ; Keep track of how many items are in the array.
    Array%ArrayCount% := A_LoopReadLine  ; Store this line in the next array element.
}

; Read from the array:
Loop %ArrayCount%
{
SetTitleMatchmode, 2 ; partial title match
    ; The following line uses the := operator to retrieve an array element:
    element := Array%A_Index%  ; A_Index is a built-in variable.
    ; Alternatively, you could use the "% " prefix to make MsgBox or some other command expression-capable:
   ; MsgBox % "Element number " . A_Index . " is " . Array%A_Index%

	WinWait, Notepad
	WinActivate, Notepad
	Send, element%A_Index% `n 
}
