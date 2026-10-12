@echo off
chcp 65001 >nul
setlocal
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
echo === 暗区突围·武装派遣 自动刷新（dry-run：只读屏算坐标，一次都不点） ===
"%~dp0.venv\Scripts\python.exe" -m darkzone.runner %*
echo.
pause
