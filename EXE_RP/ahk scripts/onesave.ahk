WinWait, Mercenary Live Feed - Google Chrome, 
IfWinNotActive, Mercenary Live Feed - Google Chrome, , WinActivate, Mercenary Live Feed - Google Chrome, 
WinWaitActive, Mercenary Live Feed - Google Chrome, 
Send, {CTRLDOWN}a{CTRLUP}{CTRLDOWN}c{CTRLUP}
WinWait, outputmerc.txt - WordPad, 
IfWinNotActive, outputmerc.txt - WordPad, , WinActivate, outputmerc.txt - WordPad, 
WinWaitActive, outputmerc.txt - WordPad, 
MouseClick, left,  51,  262
Sleep, 100
Send, {CTRLDOWN}v{CTRLUP}{ENTER}
Sleep, 100
WinWait, Mercenary Live Feed - Google Chrome, 
IfWinNotActive, Mercenary Live Feed - Google Chrome, , WinActivate, Mercenary Live Feed - Google Chrome, 
WinWaitActive, Mercenary Live Feed - Google Chrome, 
MouseClick, left,  22,  55
Sleep, 100