@echo off
where pip > nul 2>&1
if %errorlevel% equ 1 (
    echo Error: Pip is not available on this system.
    pause
    exit /b 1
)
pip show pygame > nul 2>&1
if %errorlevel% equ 1 (
    echo Installing Pygame...
    pip install pygame
)
python main.py
