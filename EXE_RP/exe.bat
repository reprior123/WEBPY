REM cd C:\Users\bob\Google Drive\EXE_RP
SET @subexe=\Google Drive\EXE_RP

SET @rootdir=%CD%
SET @rootnew=%~dp0

SET @myvar=%@rootnew%%@subexe%

cd "%@rootnew%"

