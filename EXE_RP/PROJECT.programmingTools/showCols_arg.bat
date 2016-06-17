::REM head -1 /cygdrive/z/exe/data/SFDATA/201202/*14*accounts.csv | tr "," "\n" | cat -n
set datefile=%1
::REM SET datefile=20120402
set month=201204
set DRIVE=Z
echo %datefile%

SET SFAREA=%DRIVE%:/exe/data/SFDATA/%month%/%datefile%

head -1 %SFAREA%/%datefile%.sf.accounts.csv | tr "," "\n" | cat -n 
head -1 %SFAREA%/%datefile%.sf.assets.csv | tr "," "\n" | cat -n 
