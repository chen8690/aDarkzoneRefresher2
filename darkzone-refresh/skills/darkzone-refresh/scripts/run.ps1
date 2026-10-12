# 暗区突围·武装派遣自动刷新 —— 便捷入口
# 用法（任意目录）：pwsh scripts/run.ps1 [runner 参数]
$ErrorActionPreference = "Stop"

# 定位 skill 根目录（本脚本上一级）。优先脚本自身路径，拿不到就退回当前目录。
$scriptPath = $PSCommandPath
if (-not $scriptPath) { $scriptPath = $MyInvocation.MyCommand.Definition }
if (-not $scriptPath -and $PSScriptRoot) { $scriptPath = Join-Path $PSScriptRoot "run.ps1" }

if ($scriptPath -and (Test-Path -LiteralPath $scriptPath)) {
    $scriptDir = Split-Path -Parent $scriptPath              # ...\scripts
    $root = (Resolve-Path -LiteralPath (Join-Path $scriptDir "..")).Path
    Set-Location -LiteralPath $root
} else {
    $root = (Get-Location).Path
}

# 选 Python：DARKZONE_PYTHON > 项目 .venv > PATH 里的 python
$python = $env:DARKZONE_PYTHON
if (-not $python) {
    $venvPy = Join-Path $root ".venv\Scripts\python.exe"
    if (Test-Path -LiteralPath $venvPy) { $python = $venvPy } else { $python = "python" }
}

$env:PYTHONIOENCODING = "utf-8"
& $python -m darkzone.runner @args
exit $LASTEXITCODE