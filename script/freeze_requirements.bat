@echo off

:: Delete existing requirements.txt if it exists
if exist requirements.txt del requirements.txt

:: Freeze requirements
pip freeze > requirements.txt
if %errorlevel% neq 0 (
    echo Error while freezing requirements.
) else (
    echo Requirements saved to requirements.txt
)
