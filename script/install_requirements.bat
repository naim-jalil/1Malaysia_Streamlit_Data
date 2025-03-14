@echo off

:: Set virtual environment directory
set VENV_DIR=.venv

:: Delete broken virtual env if needed
if exist %VENV_DIR% (
    if not exist %VENV_DIR%\Scripts\activate.bat (
        echo Warning: Incomplete virtual environment found. Deleting and recreating...
        rmdir /s /q %VENV_DIR%
    )
)

:: Create virtual environment
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    py -m venv %VENV_DIR%
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment. Check Python installation.
        exit /b 1
    )
)

:: Verify activation script exists
if not exist %VENV_DIR%\Scripts\activate.bat (
    echo Error: Virtual environment activation script not found!
    exit /b 1
)

:: Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat

:: Install requirements
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error while installing requirements.
) else (
    echo Requirements installed successfully.
)
