@echo off
echo ========================================
echo RepoInsight MCP - Quick Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

echo [1/4] Checking Python version...
python --version

echo.
echo [2/4] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    echo Virtual environment created
)

echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/4] Installing dependencies...
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the server:
echo   1. Activate environment: venv\Scripts\activate
echo   2. Run server: python -m repoinsight_mcp.main
echo.
echo To use with Claude Desktop:
echo   1. Edit: %%APPDATA%%\Claude\claude_desktop_config.json
echo   2. Add configuration from mcp_config_example.json
echo   3. Update paths to match your installation
echo.
echo For more details, see SETUP.md
echo.
pause
