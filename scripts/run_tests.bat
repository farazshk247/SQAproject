@echo off
setlocal EnableDelayedExpansion

REM run_tests.bat - CSCI 3060U Phase 1 test harness (Windows)
REM
REM Runs the Front End executable against every test case in ..\test_cases,
REM compares actual output to the expected files, and stores a timestamped
REM results folder under ..\results for reporting and comparison across runs.
REM
REM Usage:
REM   run_tests.bat [path-to-frontend.exe]
REM
REM Assumed Front End command-line contract (update this file + the invocation
REM below once Phase 2/3's real CLI is finalized):
REM   frontend.exe <accounts_file> <games_file> <collection_file> <daily_output_file>
REM   - reads the transaction stream on stdin
REM   - writes prompts/messages to stdout

set FRONTEND_EXE=%1
if "%FRONTEND_EXE%"=="" set FRONTEND_EXE=..\front_end\frontend.exe

set SCRIPT_DIR=%~dp0
set TEST_ROOT=%SCRIPT_DIR%..\test_cases

for /f "tokens=2-4 delims=/ " %%a in ('date /t') do set DATESTAMP=%%c%%a%%b
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIMESTAMP=%%a%%b
set STAMP=%DATESTAMP%_%TIMESTAMP%

set RESULTS_DIR=%SCRIPT_DIR%..\results\run_%STAMP%
mkdir "%RESULTS_DIR%" 2>nul

set SUMMARY=%RESULTS_DIR%\summary.txt
echo CSCI 3060U Phase 1 Test Run - %STAMP% > "%SUMMARY%"
echo Front End under test: %FRONTEND_EXE% >> "%SUMMARY%"
echo. >> "%SUMMARY%"

set PASS_COUNT=0
set FAIL_COUNT=0

for /d %%T in ("%TEST_ROOT%\test_*") do (
    set TEST_NAME=%%~nxT
    set OUT_DIR=%RESULTS_DIR%\!TEST_NAME!
    mkdir "!OUT_DIR!" 2>nul

    set ACCOUNTS=%%T\input_current_user_accounts.txt
    set GAMES=%%T\input_available_games.txt
    set COLLECTION=%%T\input_game_collection.txt
    set STREAM=%%T\input_transaction_stream.txt
    set EXP_CONSOLE=%%T\expected_console_output.txt
    set EXP_DAILY=%%T\expected_daily_transaction_file.txt
    set ACT_CONSOLE=!OUT_DIR!\actual_console_output.txt
    set ACT_DAILY=!OUT_DIR!\actual_daily_transaction_file.txt

    "%FRONTEND_EXE%" "!ACCOUNTS!" "!GAMES!" "!COLLECTION!" "!ACT_DAILY!" < "!STREAM!" > "!ACT_CONSOLE!" 2>&1

    set RESULT=PASS

    fc "!EXP_CONSOLE!" "!ACT_CONSOLE!" > "!OUT_DIR!\diff_console.txt"
    if not !errorlevel! == 0 set RESULT=FAIL

    findstr /b "N/A" "!EXP_DAILY!" >nul
    if !errorlevel! == 0 (
        if exist "!ACT_DAILY!" (
            echo Daily transaction file was written but none was expected. > "!OUT_DIR!\diff_daily_transaction.txt"
            set RESULT=FAIL
        )
    ) else (
        fc "!EXP_DAILY!" "!ACT_DAILY!" > "!OUT_DIR!\diff_daily_transaction.txt"
        if not !errorlevel! == 0 set RESULT=FAIL
    )

    echo !RESULT! > "!OUT_DIR!\RESULT.txt"
    echo !TEST_NAME! - !RESULT! >> "%SUMMARY%"

    if "!RESULT!"=="PASS" (
        set /a PASS_COUNT+=1
    ) else (
        set /a FAIL_COUNT+=1
    )
)

echo. >> "%SUMMARY%"
echo Passed: %PASS_COUNT%  Failed: %FAIL_COUNT% >> "%SUMMARY%"

type "%SUMMARY%"
echo.
echo Full results stored in: %RESULTS_DIR%
