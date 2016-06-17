echo off 
echo %1
cat newassets | grep "%1"  

cat newassets | grep "%1"  > bla
wc bla
cat bla

REM>>namesgrepped