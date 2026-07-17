# 功放测试系统启动脚本 (PowerShell)
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  功放测试系统启动" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$RootDir = $PSScriptRoot

Write-Host "[1/2] 启动后端服务..." -ForegroundColor Green
$BackendDir = Join-Path $RootDir "backend"
Set-Location $BackendDir
pip install -r requirements.txt -q
python init_mock_data.py
Start-Process python -ArgumentList "run.py"

Start-Sleep -Seconds 2

Write-Host "[2/2] 启动前端服务..." -ForegroundColor Green
$FrontendDir = Join-Path $RootDir "frontend"
Set-Location $FrontendDir
npm install
Start-Process npm -ArgumentList "run dev"

Set-Location $RootDir

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  启动完成！" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "后端地址: http://localhost:5000" -ForegroundColor Yellow
Write-Host "前端地址: http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
