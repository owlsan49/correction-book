@echo off

set PYTHON=C:\CustomProgram\Anaconda3\envs\vocab\python.exe
cd ./cb-back
start cmd.exe /k %PYTHON% app.py
cd ..
cd ./cb-front
start cmd.exe /k npm run dev
start http://localhost:5173/