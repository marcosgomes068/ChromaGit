@echo off
REM Script de teste para verificar instalação do ChromaGit
echo ====================================
echo     Teste de Instalacao ChromaGit
echo ====================================
echo.

echo [1/4] Verificando PATH do sistema...
echo %PATH% | findstr /i chromagit >nul
if %errorlevel%==0 (
    echo ✓ ChromaGit encontrado no PATH do sistema
) else (
    echo ✗ ChromaGit NAO encontrado no PATH do sistema
)

echo.
echo [2/4] Verificando PATH do usuario...
for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\Environment" /v PATH 2^>nul') do set "UserPath=%%b"
echo %UserPath% | findstr /i chromagit >nul
if %errorlevel%==0 (
    echo ✓ ChromaGit encontrado no PATH do usuario
) else (
    echo ✗ ChromaGit NAO encontrado no PATH do usuario
)

echo.
echo [3/4] Verificando arquivos...
if exist "obj\ChromaGit.exe" (
    echo ✓ ChromaGit.exe encontrado
) else (
    echo ✗ ChromaGit.exe NAO encontrado
)

if exist "obj\chromagit.bat" (
    echo ✓ chromagit.bat encontrado
) else (
    echo ✗ chromagit.bat NAO encontrado
)

echo.
echo [4/4] Testando execucao...
obj\chromagit.bat --version >nul 2>&1
if %errorlevel%==0 (
    echo ✓ ChromaGit executa corretamente
    echo.
    echo Versao instalada:
    obj\chromagit.bat --version
) else (
    echo ✗ Erro ao executar ChromaGit
)

echo.
echo ====================================
echo           Resultado Final
echo ====================================
echo.
echo Para usar ChromaGit globalmente:
echo 1. Feche este terminal
echo 2. Abra um novo terminal
echo 3. Digite: chromagit --version
echo.
echo Comandos disponiveis:
echo   chromagit init
echo   chromagit add .
echo   chromagit commit -m "mensagem"
echo   chromagit log
echo   chromagit push
echo   chromagit --help
echo.
pause
