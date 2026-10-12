@echo off
chcp 65001 >nul
setlocal
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
echo === 暗区突围·武装派遣 自动刷新（LIVE：真正点击，三行就绪后停手，不点派遣） ===
echo     每行刷新上限 40 次；想改次数：run_live.bat --limit 20
echo     中途要停：直接关窗口 / Ctrl+C
echo.
"%~dp0.venv\Scripts\python.exe" -m darkzone.runner --live %*
echo.
pause
