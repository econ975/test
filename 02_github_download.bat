@echo off
CHCP 65001
set /p github_address=enter GitHub repository address:
set /p github_branch=enter branch:
PortableGit\bin\git.exe clone -b %github_branch% %github_address% temp
echo finish
pause
