@echo off
setlocal enabledelayedexpansion
set "message=%*"
git add .
git commit -m "!message!"
git push origin master
