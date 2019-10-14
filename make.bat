@echo off

if [%1] == [] goto help

REM This allows us to expand variables at execution
setlocal ENABLEDELAYEDEXPANSION

REM This will set PYFILES as a list of tracked .py files
set PYFILES=
for /F "tokens=* USEBACKQ" %%A in (`git ls-files "*.py"`) do (
    set PYFILES=!PYFILES! %%A
)

goto %1

:reformat
python -m black -l 99 --target-version py37 !PYFILES!
exit /B %ERRORLEVEL%

:stylecheck
python -m black -l 99 --check --target-version py37 !PYFILES!
exit /B %ERRORLEVEL%

:newenv
py -3.7 -m venv --clear .venv
".venv\Scripts\python.exe" -m pip install -U pip setuptools
goto syncenv

:syncenv
".venv\Scripts\pip.exe" install --upgrade --editable .[dev]
exit /B %ERRORLEVEL%

:help
echo Usage:
echo   make ^<command^>
echo.
echo Commands:
echo   reformat                   Reformat all .py files being tracked by git.
echo   stylecheck                 Check which tracked .py files need reformatting.
echo   newenv                     Create or replace this project's virtual environment.
echo   syncenv                    Sync this project's virtual environment with its latest
echo                              dependencies.
