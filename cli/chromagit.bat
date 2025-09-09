@echo off
setlocal enabledelayedexpansion

:: ChromaGit CLI Installer/Runner
:: Facilita o uso do ChromaGit CLI

set "SCRIPT_DIR=%~dp0"
set "OBJ_DIR=%SCRIPT_DIR%..\obj"
set "CLI_SCRIPT=%SCRIPT_DIR%chromagit.py"

:: Verifica se Python está disponível
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python nao encontrado. Instale Python 3.7+ primeiro.
    pause
    exit /b 1
)

:: Verifica se o arquivo CLI existe
if not exist "%CLI_SCRIPT%" (
    echo [ERROR] chromagit.py nao encontrado em %CLI_SCRIPT%
    pause
    exit /b 1
)

:: Verifica se os executáveis existem
set "MISSING_EXES="
for %%E in (init.exe add.exe commit.exe log.exe push.exe help.exe) do (
    if not exist "%OBJ_DIR%\%%E" (
        set "MISSING_EXES=!MISSING_EXES! %%E"
    )
)

if defined MISSING_EXES (
    echo [WARNING] Alguns executaveis nao foram encontrados em %OBJ_DIR%:
    echo !MISSING_EXES!
    echo.
    echo Compile os arquivos Python primeiro ou verifique o caminho.
    echo.
)

:: Executa o ChromaGit CLI
echo [INFO] Iniciando ChromaGit CLI...
echo.

python "%CLI_SCRIPT%" %*

:: Pausa apenas se executado diretamente (duplo-clique)
if "%~1"=="" (
    echo.
    pause
)
