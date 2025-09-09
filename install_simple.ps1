# ChromaGit - Instalador Simples de Todos os Executáveis
param(
    [switch]$User,
    [switch]$System,
    [switch]$Remove
)

function Write-Status {
    param([string]$Message, [string]$Type = "Info")
    
    $color = switch ($Type) {
        "Success" { "Green" }
        "Error" { "Red" }
        "Warning" { "Yellow" }
        "Info" { "Cyan" }
        default { "White" }
    }
    
    Write-Host $Message -ForegroundColor $color
}

function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Create-BatchFiles {
    param([string]$ObjPath)
    
    Write-Status "Criando arquivos .bat para todos os executáveis..." "Info"
    
    # Lista de executáveis para criar launchers
    $exeList = @("add", "commit", "help", "init", "log", "push")
    $created = 0
    
    # Criar launcher para cada executável
    foreach ($exeName in $exeList) {
        $exePath = Join-Path $ObjPath "$exeName.exe"
        $batPath = Join-Path $ObjPath "$exeName.bat"
        
        if (Test-Path $exePath) {
            $content = "@echo off`r`n"
            $content += "`"$exePath`" %*`r`n"
            
            try {
                $content | Out-File -FilePath $batPath -Encoding ASCII -Force
                Write-Status "  Criado: $exeName.bat" "Success"
                $created++
            }
            catch {
                Write-Status "  Erro ao criar: $exeName.bat" "Error"
            }
        }
    }
    
    # Criar launcher principal chromagit
    $chromaGitExe = Join-Path $ObjPath "ChromaGit.exe"
    $chromaGitBat = Join-Path $ObjPath "chromagit.bat"
    
    if (Test-Path $chromaGitExe) {
        $content = "@echo off`r`n"
        $content += "`"$chromaGitExe`" %*`r`n"
        
        try {
            $content | Out-File -FilePath $chromaGitBat -Encoding ASCII -Force
            Write-Status "  Criado: chromagit.bat" "Success"
            $created++
        }
        catch {
            Write-Status "  Erro ao criar: chromagit.bat" "Error"
        }
    }
    
    Write-Status "Total de launchers criados: $created" "Success"
    return $created
}

function Add-ToPath {
    param([string]$Path, [string]$Scope)
    
    Write-Status "Adicionando ao PATH do $Scope..." "Info"
    
    $currentPath = [Environment]::GetEnvironmentVariable("PATH", $Scope)
    
    if ($currentPath -like "*$Path*") {
        Write-Status "Já existe no PATH do $Scope" "Warning"
        return $true
    }
    
    try {
        $newPath = "$Path;$currentPath"
        [Environment]::SetEnvironmentVariable("PATH", $newPath, $Scope)
        Write-Status "Adicionado ao PATH do $Scope com sucesso!" "Success"
        return $true
    }
    catch {
        Write-Status "Erro ao adicionar ao PATH: $_" "Error"
        return $false
    }
}

function Remove-FromPath {
    param([string]$Path)
    
    Write-Status "Removendo do PATH..." "Warning"
    
    # Remover do usuário
    $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
    if ($userPath -like "*$Path*") {
        $newUserPath = $userPath.Replace("$Path;", "").Replace(";$Path", "").Replace($Path, "")
        [Environment]::SetEnvironmentVariable("PATH", $newUserPath, "User")
        Write-Status "Removido do PATH do usuário" "Success"
    }
    
    # Remover do sistema (se admin)
    if (Test-Admin) {
        $systemPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
        if ($systemPath -like "*$Path*") {
            $newSystemPath = $systemPath.Replace("$Path;", "").Replace(";$Path", "").Replace($Path, "")
            [Environment]::SetEnvironmentVariable("PATH", $newSystemPath, "Machine")
            Write-Status "Removido do PATH do sistema" "Success"
        }
    }
    
    # Remover arquivos .bat
    $objPath = $Path
    $batFiles = @("add.bat", "commit.bat", "help.bat", "init.bat", "log.bat", "push.bat", "chromagit.bat")
    
    foreach ($batFile in $batFiles) {
        $fullPath = Join-Path $objPath $batFile
        if (Test-Path $fullPath) {
            Remove-Item $fullPath -Force
            Write-Status "Removido: $batFile" "Success"
        }
    }
}

function Test-Commands {
    param([string]$ObjPath)
    
    Write-Status "Testando comandos..." "Info"
    
    $commands = @("chromagit", "add", "commit", "help", "init", "log", "push")
    $working = 0
    
    foreach ($cmd in $commands) {
        $batFile = Join-Path $ObjPath "$cmd.bat"
        if (Test-Path $batFile) {
            Write-Status "  $cmd - OK" "Success"
            $working++
        } else {
            Write-Status "  $cmd - Não encontrado" "Error"
        }
    }
    
    Write-Status "Comandos funcionais: $working de $($commands.Count)" "Info"
    return $working
}

# MAIN
Write-Host "╭─────────────────────────────────────────────╮" -ForegroundColor Cyan
Write-Host "│    ChromaGit - Instalador de Executáveis    │" -ForegroundColor Cyan
Write-Host "│      Adicionar TODOS os comandos ao PATH    │" -ForegroundColor Cyan
Write-Host "╰─────────────────────────────────────────────╯" -ForegroundColor Cyan
Write-Host ""

# Verificar diretório obj
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$objDir = Join-Path $scriptDir "obj"

if (-not (Test-Path $objDir)) {
    Write-Status "Diretório obj/ não encontrado!" "Error"
    Write-Status "Execute este script na pasta raiz do ChromaGit" "Warning"
    exit 1
}

Write-Status "ChromaGit encontrado em: $objDir" "Success"

# Listar executáveis
$exeFiles = Get-ChildItem -Path $objDir -Filter "*.exe" | Where-Object { $_.Name -ne "ChromaGit-Desktop.exe" }
Write-Status "Executáveis encontrados: $($exeFiles.Count)" "Info"
foreach ($exe in $exeFiles) {
    Write-Status "  $($exe.Name)" "Info"
}
Write-Host ""

# Processar opções
if ($Remove) {
    Remove-FromPath $objDir
}
elseif ($System) {
    if (-not (Test-Admin)) {
        Write-Status "Privilégios de administrador necessários para PATH do sistema!" "Error"
        exit 1
    }
    Create-BatchFiles $objDir
    Add-ToPath $objDir "Machine"
}
elseif ($User) {
    Create-BatchFiles $objDir
    Add-ToPath $objDir "User"
}
else {
    # Menu interativo
    Write-Status "Escolha uma opção:" "Info"
    Write-Host "1. Instalar no PATH do usuário (recomendado)"
    Write-Host "2. Instalar no PATH do sistema (requer admin)"
    Write-Host "3. Remover do PATH"
    Write-Host "4. Testar instalação"
    Write-Host "5. Cancelar"
    Write-Host ""
    
    $choice = Read-Host "Digite sua escolha (1-5)"
    
    switch ($choice) {
        "1" {
            Create-BatchFiles $objDir
            Add-ToPath $objDir "User"
        }
        "2" {
            if (-not (Test-Admin)) {
                Write-Status "Execute como administrador para PATH do sistema!" "Error"
                exit 1
            }
            Create-BatchFiles $objDir
            Add-ToPath $objDir "Machine"
        }
        "3" {
            Remove-FromPath $objDir
        }
        "4" {
            Test-Commands $objDir
            exit 0
        }
        "5" {
            Write-Status "Cancelado" "Warning"
            exit 0
        }
        default {
            Write-Status "Opção inválida!" "Error"
            exit 1
        }
    }
}

Write-Host ""
Write-Status "Testando instalação..." "Info"
$workingCount = Test-Commands $objDir

Write-Host ""
Write-Host "╭─────────────────────────────────────────────╮" -ForegroundColor Green
Write-Host "│              Instalação Concluída!          │" -ForegroundColor Green
Write-Host "╰─────────────────────────────────────────────╯" -ForegroundColor Green
Write-Host ""

Write-Status "Comandos disponíveis após reiniciar terminal:" "Info"
Write-Host "  chromagit --version      # Versão"
Write-Host "  chromagit init           # Inicializar"
Write-Host "  add .                    # Adicionar arquivos"
Write-Host "  commit -m 'msg'          # Fazer commit"
Write-Host "  log                      # Ver histórico"
Write-Host "  push                     # Sincronizar"
Write-Host "  help                     # Ajuda"

Write-Host ""
Write-Status "IMPORTANTE: Reinicie o terminal para usar os comandos!" "Warning"
Write-Status "Para usar agora: `$env:PATH = '$objDir;' + `$env:PATH" "Info"
