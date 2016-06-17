::REM 
SET datefile=20120614
set month=201206
set DRIVE=Y
echo %datefile%

SET SFAREA=%DRIVE%:/exe/data/SFDATA/%month%/%datefile%

head -1 %SFAREA%/%datefile%.sf.accounts.csv | tr "," "\n" | cat -n 
head -1 %SFAREA%/%datefile%.sf.assets.csv | tr "," "\n" | cat -n 
head -1 %SFAREA%/%datefile%.sf.Opportunities.csv | tail -1 | tr "," "\n" | cat -n > bla.txt
head -1 %SFAREA%/%datefile%.sf.Opportunities.csv | tail -1 | tr "," "\n" | gawk `{print "ff",$0}`
