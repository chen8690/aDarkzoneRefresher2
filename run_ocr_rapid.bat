@echo off
chcp 65001 >nul
setlocal
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"
echo === 暗区突围·武装派遣 自动刷新（RapidOCR 引擎：更准，但每屏约 10 秒） ===
echo     用法同 dry_run.bat / run_live.bat：不带参数=预演；加 --live 才是真刷。
echo     例：run_ocr_rapid.bat --live --limit 30 --no-sweep
echo.
"%~dp0.venv\Scripts\python.exe" -m darkzone.runner --ocr rapid %*
echo.
pause
