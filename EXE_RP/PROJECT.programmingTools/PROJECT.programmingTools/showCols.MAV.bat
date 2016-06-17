::REM head -1 /cygdrive/z/exe/data/SFDATA/201202/*14*accounts.csv | tr "," "\n" | cat -n
SET SFAREA=y:/exe/data/SFDATA/20120319

::REMgrep MAVENDER %SFAREA%/*20120315*accounts.csv | tr "," "\n" | cat -n 
head -1 %SFAREA%/*20120319*assets.csv | tr "," "\n" | cat -n

ls %SFAREA%/*.csv 

::REM grep 0012000000hjEs0AAE %SFAREA%/*20120315*assets.csv | grep -i production | tail -1 | tr "," "\n" | cat -n 


::REMgrep  02i2000000ITuxhAAD %SFAREA%/*20120315*assets.csv | tr "," "\n" | cat -n 

::REMgrep 01t20000002NQUz %SFAREA%/*20120315*assets.csv | grep -i trading  | wc
::REM grep 0 %SFAREA%/*20120315*assets.csv | grep -i production | wc
::REMgrep 01t20000002NQUz %SFAREA%/*20120315*assets.csv | grep -i trading  | tr "," "\n" | cat -n 
