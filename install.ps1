# ChromaGit Windows Installer
# PowerShell script for Windows installation

param(
    [switch]$Force,
    [string]$InstallPath = "$env:LOCALAPPDATA\ChromaGit"
)

# Colors for console output
$Colors = @{
    Red = "Red"
    Green = "Green" 
    Yellow = "Yellow"
    Blue = "Blue"
    Cyan = "Cyan"
}

function Write-Header {
    Write-Host "╭─────────────────────────────────────────────╮" -ForegroundColor $Colors.Blue
    Write-Host "│           ChromaGit Installer               │" -ForegroundColor $Colors.Blue
    Write-Host "│        Sistema de Controle de Versão        │" -ForegroundColor $Colors.Blue
    Write-Host "╰─────────────────────────────────────────────╯" -ForegroundColor $Colors.Blue
}

function Write-Step {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Colors.Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Colors.Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Colors.Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Colors.Red
}

function Test-Python {
    Write-Step "Verificando instalação do Python..."
    
    $pythonCommands = @("python", "python3", "py")
    $pythonFound = $false
    
    foreach ($cmd in $pythonCommands) {
        try {
            $version = & $cmd --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Python encontrado: $version"
                $script:PythonCmd = $cmd
                $pythonFound = $true
                break
            }
        }
        catch {
            continue
        }
    }
    
    if (-not $pythonFound) {
        Write-Error "Python não encontrado. Instale Python 3.8+ de https://python.org"
        exit 1
    }
    
    # Check version
    try {
        $versionOutput = & $script:PythonCmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        $versionParts = $versionOutput.Split('.')
        $major = [int]$versionParts[0]
        $minor = [int]$versionParts[1]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-Error "Python 3.8+ é necessário. Versão atual: $versionOutput"
            exit 1
        }
    }
    catch {
        Write-Error "Erro ao verificar versão do Python"
        exit 1
    }
}

function Test-Pip {
    Write-Step "Verificando pip..."
    
    try {
        & $script:PythonCmd -m pip --version | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "pip encontrado"
        }
        else {
            throw "pip não encontrado"
        }
    }
    catch {
        Write-Error "pip não encontrado. Instale pip antes de continuar."
        exit 1
    }
}

function Install-Dependencies {
    Write-Step "Instalando dependências..."
    
    $packages = @("rich", "pathlib")
    
    foreach ($package in $packages) {
        try {
            Write-Host "  Instalando $package..." -ForegroundColor $Colors.Cyan
            & $script:PythonCmd -m pip install --user $package
            if ($LASTEXITCODE -ne 0) {
                throw "Falha ao instalar $package"
            }
        }
        catch {
            Write-Error "Falha ao instalar $package"
            exit 1
        }
    }
    
    Write-Success "Dependências instaladas"
}

function Install-ChromaGit {
    Write-Step "Instalando ChromaGit..."
    
    if (Test-Path $InstallPath) {
        if ($Force) {
            Write-Warning "Removendo instalação anterior..."
            Remove-Item -Recurse -Force $InstallPath
        }
        else {
            Write-Warning "ChromaGit já instalado em $InstallPath"
            $response = Read-Host "Deseja reinstalar? (y/N)"
            if ($response -notmatch "^[Yy]$") {
                Write-Step "Instalação cancelada"
                exit 0
            }
            Remove-Item -Recurse -Force $InstallPath
        }
    }
    
    # Create installation directory
    New-Item -ItemType Directory -Force -Path $InstallPath | Out-Null
    
    # Copy files
    $sourceFiles = @("main.py", "obj", "cli", "docs", "pyproject.toml", "README.md", "LICENSE")
    
    foreach ($item in $sourceFiles) {
        if (Test-Path $item) {
            Write-Host "  Copiando $item..." -ForegroundColor $Colors.Cyan
            Copy-Item -Recurse -Force $item $InstallPath
        }
    }
    
    Write-Success "ChromaGit instalado em $InstallPath"
}

function Add-ToPath {
    Write-Step "Adicionando ao PATH..."
    
    # Check if already in PATH
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($currentPath -notlike "*$InstallPath*") {
        $newPath = "$InstallPath;$currentPath"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Success "ChromaGit adicionado ao PATH"
        Write-Warning "Reinicie o terminal para usar 'chromagit' diretamente"
    }
    else {
        Write-Success "ChromaGit já está no PATH"
    }
}

function Create-Launcher {
    Write-Step "Criando launcher..."
    
    # Create batch file for easy access
    $batchContent = @"
@echo off
"$script:PythonCmd" "$InstallPath\main.py" %*
"@
    
    $batchPath = "$InstallPath\chromagit.bat"
    $batchContent | Out-File -FilePath $batchPath -Encoding ASCII
    
    Write-Success "Launcher criado: $batchPath"
}

function Test-Installation {
    Write-Step "Testando instalação..."
    
    try {
        $testOutput = & $script:PythonCmd "$InstallPath\main.py" --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "ChromaGit instalado e funcionando corretamente!"
        }
        else {
            throw "Erro no teste"
        }
    }
    catch {
        Write-Error "Erro na instalação. ChromaGit não está funcionando."
        Write-Host "Saída: $testOutput" -ForegroundColor $Colors.Red
        exit 1
    }
}

function Show-Usage {
    Write-Host ""
    Write-Host "╭─────────────────────────────────────────────╮" -ForegroundColor $Colors.Green
    Write-Host "│             Instalação Concluída!           │" -ForegroundColor $Colors.Green
    Write-Host "╰─────────────────────────────────────────────╯" -ForegroundColor $Colors.Green
    Write-Host ""
    
    Write-Host "Como usar:" -ForegroundColor $Colors.Blue
    Write-Host "  chromagit                    # Modo interativo"
    Write-Host "  chromagit init               # Inicializar repositório"
    Write-Host "  chromagit add .              # Adicionar arquivos"
    Write-Host "  chromagit commit -m `"msg`"    # Fazer commit"
    Write-Host "  chromagit push               # Sincronizar"
    Write-Host "  chromagit --help             # Ajuda"
    Write-Host ""
    
    Write-Host "Caminhos diretos:" -ForegroundColor $Colors.Blue
    Write-Host "  python `"$InstallPath\main.py`""
    Write-Host "  `"$InstallPath\chromagit.bat`""
    Write-Host ""
    
    Write-Host "Documentação:" -ForegroundColor $Colors.Blue
    Write-Host "  $InstallPath\docs\"
    Write-Host ""
    
    Write-Host "Desinstalar:" -ForegroundColor $Colors.Blue
    Write-Host "  Remove-Item -Recurse -Force `"$InstallPath`""
}

# Main installation process
function Main {
    Write-Header
    
    # Check if running as Administrator
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    if ($isAdmin) {
        Write-Warning "Executando como Administrador não é necessário"
    }
    
    Test-Python
    Test-Pip
    Install-Dependencies
    Install-ChromaGit
    Add-ToPath
    Create-Launcher
    Test-Installation
    Show-Usage
    
    Write-Success "ChromaGit instalado com sucesso!"
}

# Run main function
Main
