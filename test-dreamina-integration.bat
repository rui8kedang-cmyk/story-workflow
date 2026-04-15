@echo off
REM Dreamina 集成测试脚本
REM 用于验证 story-workflow 项目的 Dreamina 集成

echo =============================
echo Dreamina 集成测试
echo =============================

REM 检查 PATH 是否包含 Dreamina
echo 检查 Dreamina CLI 安装...
where dreamina >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Dreamina CLI 未找到，请确保已正确安装
    pause
    exit /b 1
)

REM 检查登录状态
echo 检查登录状态...
dreamina login --headless
if %errorlevel% neq 0 (
    echo 错误: 登录失败
    pause
    exit /b 1
)

REM 检查积分余额
echo 检查积分余额...
dreamina user_credit

REM 测试帮助命令
echo 测试命令帮助...
dreamina multimodal2video -h >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: multimodal2video 命令不可用
    pause
    exit /b 1
)

echo.
echo =============================
echo ✅ Dreamina 集成测试通过！
echo 现在可以使用 Seedance 2.0 全能参考模式
echo =============================

pause