::REM head -1 /cygdrive/z/exe/data/SFDATA/201202/*14*accounts.csv | tr "," "\n" | cat -n
SET datefile=20120402
set month=201204
set DRIVE=Y
echo %datefile%

SET SFAREA=%DRIVE%:/exe/data/SFDATA/%month%/%datefile%

head -1 %SFAREA%/%datefile%.sf.contacts.csv | tr "," "\n" | cat -n 
