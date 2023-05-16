@echo off
echo Checking libraries...

python -c "import tabulate" > nul 2>&1
if %errorlevel% equ 0 (
    echo tabulate is installed
) else (
    echo tabulate is not installed
    set /p choice="Do you want to install tabulate (Y/n)"
    if "%choice%" equ "Y" (
        pip install tabulate
    ) 
    if "%choice%" equ "y" (
        pip install tabulate
    ) 
    if "%choice%" equ "n" (
        exit /b
    )  
)
python -c "import lark" > nul 2>&1
if %errorlevel% equ 0 (
    echo lark is installed
) else (
    echo lark is not installed
    set /p choice="Do you want to install lark (Y/n)"
    if "%choice%" equ "Y" (
        pip install lark 
    ) 
    if "%choice%" equ "y" (
        pip install lark
    ) 
    if "%choice%" equ "n" (
        exit /b
    )  
)
echo Successfully install all libraries
python3 iengine.py %1 %2
