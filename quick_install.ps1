# Instalador ChromaGit - Simples
param([switch]$User, [switch]$System, [switch]$Remove)

Write-Host "ChromaGit - Instalador de Executaveis" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan

$objDir = Join-Path $PSScriptRoot "obj"

if (-not (Test-Path $objDir)) {
    Write-Host "Erro: Diretorio obj/ nao encontrado!" -ForegroundColor Red
    exit 1
}

Write-Host "ChromaGit encontrado em: $objDir" -ForegroundColor Green

function CreateBatFiles {
    param($path)
    
    Write-Host "Criando arquivos .bat..." -ForegroundColor Yellow
    
    $commands = @("add", "commit", "help", "init", "log", "push")
    $created = 0
    
    foreach ($cmd in $commands) {
        $exePath = Join-Path $path "$cmd.exe"
        $batPath = Join-Path $path "$cmd.bat"
        
        if (Test-Path $exePath) {
            "@echo off`r`n`"$exePath`" %*" | Out-File -FilePath $batPath -Encoding ASCII
            Write-Host "  $cmd.bat criado" -ForegroundColor Green
            $created++
        }
    }
    
    # ChromaGit principal
    $chromagitExe = Join-Path $path "ChromaGit.exe"
    $chromagitBat = Join-Path $path "chromagit.bat"
    
    if (Test-Path $chromagitExe) {
        "@echo off`r`n`"$chromagitExe`" %*" | Out-File -FilePath $chromagitBat -Encoding ASCII
        Write-Host "  chromagit.bat criado" -ForegroundColor Green
        $created++
    }
    
    Write-Host "Total criados: $created" -ForegroundColor Cyan
}

function AddToPath {
    param($path, $scope)
    
    Write-Host "Adicionando ao PATH do $scope..." -ForegroundColor Yellow
    
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", $scope)
    
    if ($currentPath -like "*$path*") {
        Write-Host "Ja existe no PATH" -ForegroundColor Yellow
        return
    }
    
    $newPath = "$path;$currentPath"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, $scope)
    Write-Host "Adicionado com sucesso!" -ForegroundColor Green
}

function RemoveFromPath {
    param($path)
    
    Write-Host "Removendo do PATH..." -ForegroundColor Yellow
    
    # Usuario
    $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($userPath -like "*$path*") {
        $newPath = $userPath.Replace("$path;", "").Replace(";$path", "").Replace($path, "")
        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
        Write-Host "Removido do PATH do usuario" -ForegroundColor Green
    }
    
    # Sistema
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if ($isAdmin) {
        $systemPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
        if ($systemPath -like "*$path*") {
            $newPath = $systemPath.Replace("$path;", "").Replace(";$path", "").Replace($path, "")
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
            Write-Host "Removido do PATH do sistema" -ForegroundColor Green
        }
    }
    
    # Remover .bat files
    $batFiles = @("add.bat", "commit.bat", "help.bat", "init.bat", "log.bat", "push.bat", "chromagit.bat")
    foreach ($bat in $batFiles) {
        $batPath = Join-Path $path $bat
        if (Test-Path $batPath) {
            Remove-Item $batPath -Force
            Write-Host "Removido: $bat" -ForegroundColor Green
        }
    }
}

# Processar argumentos
if ($Remove) {
    RemoveFromPath $objDir
    Write-Host "Remocao concluida!" -ForegroundColor Green
    exit 0
}

if ($System) {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if (-not $isAdmin) {
        Write-Host "Erro: Privilegios de administrador necessarios!" -ForegroundColor Red
        exit 1
    }
    
    CreateBatFiles $objDir
    AddToPath $objDir "Machine"
    Write-Host "Instalacao no sistema concluida!" -ForegroundColor Green
    exit 0
}

if ($User) {
    CreateBatFiles $objDir
    AddToPath $objDir "User"
    Write-Host "Instalacao do usuario concluida!" -ForegroundColor Green
    exit 0
}

# Menu interativo
Write-Host ""
Write-Host "Escolha uma opcao:"
Write-Host "1. Instalar no PATH do usuario"
Write-Host "2. Instalar no PATH do sistema (requer admin)"
Write-Host "3. Remover do PATH"
Write-Host "4. Cancelar"

$choice = Read-Host "Digite (1-4)"

switch ($choice) {
    "1" {
        CreateBatFiles $objDir
        AddToPath $objDir "User"
        Write-Host "Instalacao concluida!" -ForegroundColor Green
    }
    "2" {
        $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
        $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        
        if (-not $isAdmin) {
            Write-Host "Execute como administrador!" -ForegroundColor Red
            exit 1
        }
        
        CreateBatFiles $objDir
        AddToPath $objDir "Machine"
        Write-Host "Instalacao no sistema concluida!" -ForegroundColor Green
    }
    "3" {
        RemoveFromPath $objDir
        Write-Host "Remocao concluida!" -ForegroundColor Green
    }
    "4" {
        Write-Host "Cancelado" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "Opcao invalida!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Comandos disponiveis apos reiniciar terminal:" -ForegroundColor Cyan
Write-Host "  chromagit --version"
Write-Host "  chromagit init"
Write-Host "  add ."
Write-Host "  commit -m 'mensagem'"
Write-Host "  log"
Write-Host "  push"
Write-Host "  help"

Write-Host ""
Write-Host "IMPORTANTE: Reinicie o terminal!" -ForegroundColor Yellow
Write-Host "Para usar agora execute:" -ForegroundColor Cyan
Write-Host "`$env:PATH = '$objDir;' + `$env:PATH" -ForegroundColor Green
