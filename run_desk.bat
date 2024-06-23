@echo off
chcp 65001 > nul
echo 请选择:
echo 1.singleperson_step1
echo 2.singleperson_step2
echo 3.clean_dataset_by_hand
echo 4.edit env

set /p input="请输入："

if "%input%"=="1" (
    .\env\python.exe single_person_step1.py
    if %ERRORLEVEL% NEQ 0 (
        echo something got wrong。
        pause
        exit /b %ERRORLEVEL%
    )
) else if "%input%"=="2" (
    .\env\python.exe single_person_step2.py
    if %ERRORLEVEL% NEQ 0 (
        echo something got wrong。
        pause
        exit /b %ERRORLEVEL%
    )
) else if "%input%"=="3" (
    .\env\python.exe subfix_webui_zh.py --load_list ./esd.list
) else if "%input%"=="4" (
    cd /d %~dp0
    cd .\env\Scripts
    echo 请在新打开的页面进行环境配置
    start cmd
) else if "%input%"=="esr" (
    start D:\program\RealESR-GAN
) else if "%input%"=="desk" (
    start D:\program
) else if "%input%"=="label" (
    start D:\program\auto_DataLabeling
) else (
    echo 未找到匹配项
)

echo 按回车退出...
pause
