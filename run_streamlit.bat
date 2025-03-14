@echo off

:: Set virtual environment directory
set VENV_DIR=.venv

:: Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat

:: Run Streamlit
streamlit run Home.py