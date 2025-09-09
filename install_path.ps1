Write-Host "ChromaGit PATH Installer" -ForegroundColor Cyan
Write-Host "========================" -ForegroundColor Cyan

$chromaGitDir = Join-Path (Get-Location) "obj"

if (-not (Test-Path $chromaGitDir)) {
    Write-Host "Erro: Diretório obj/ não encontrado" -ForegroundColor Red
    Write-Host "Execute este script na pasta raiz do ChromaGit" -ForegroundColor Yellow
    exit 1
}

$chromaGitExe = Join-Path $chromaGitDir "ChromaGit.exe"
if (-not (Test-Path $chromaGitExe)) {
    Write-Host "Erro: ChromaGit.exe não encontrado" -ForegroundColor Red
    Write-Host "Execute 'python build_simple.py' primeiro" -ForegroundColor Yellow
    exit 1
}

Write-Host "ChromaGit encontrado em: $chromaGitDir" -ForegroundColor Green
Write-Host ""

Write-Host "Escolha uma opção:" -ForegroundColor Blue
Write-Host "1. Adicionar ao PATH do usuário (recomendado)" -ForegroundColor White
Write-Host "2. Adicionar ao PATH do sistema (requer admin)" -ForegroundColor White  
Write-Host "3. Remover do PATH" -ForegroundColor White
Write-Host "4. Cancelar" -ForegroundColor White

$choice = Read-Host "Digite sua escolha (1-4)"

switch ($choice) {
    "1" {
        Write-Host "Adicionando ao PATH do usuário..." -ForegroundColor Blue
        $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        
        if ($userPath -like "*$chromaGitDir*") {
            Write-Host "ChromaGit já está no PATH do usuário" -ForegroundColor Green
        } else {
            if ([string]::IsNullOrEmpty($userPath)) {
                $newPath = $chromaGitDir
            } else {
                $newPath = $chromaGitDir + ";" + $userPath
            }
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
            Write-Host "ChromaGit adicionado ao PATH do usuário!" -ForegroundColor Green
            
            # Criar batch file
            $batchPath = Join-Path $chromaGitDir "chromagit.bat"
            $batchContent = "@echo off`nREM ChromaGit Launcher`nif exist `"$chromaGitDir\ChromaGit.exe`" (`n    `"$chromaGitDir\ChromaGit.exe`" %*`n) else (`n    echo Erro: ChromaGit.exe nao encontrado`n    exit /b 1`n)"
            $batchContent | Out-File -FilePath $batchPath -Encoding ASCII -Force
            Write-Host "Script chromagit.bat criado" -ForegroundColor Green
        }
    }
    "2" {
        $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
        $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        
        if (-not $isAdmin) {
            Write-Host "Erro: Privilégios de administrador necessários" -ForegroundColor Red
            Write-Host "Execute como administrador" -ForegroundColor Yellow
            exit 1
        }
        
        Write-Host "Adicionando ao PATH do sistema..." -ForegroundColor Blue
        $systemPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
        
        if ($systemPath -like "*$chromaGitDir*") {
            Write-Host "ChromaGit já está no PATH do sistema" -ForegroundColor Green
        } else {
            $newPath = $chromaGitDir + ";" + $systemPath
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "Machine")
            Write-Host "ChromaGit adicionado ao PATH do sistema!" -ForegroundColor Green
            
            # Criar batch file
            $batchPath = Join-Path $chromaGitDir "chromagit.bat"
            $batchContent = "@echo off`nREM ChromaGit Launcher`nif exist `"$chromaGitDir\ChromaGit.exe`" (`n    `"$chromaGitDir\ChromaGit.exe`" %*`n) else (`n    echo Erro: ChromaGit.exe nao encontrado`n    exit /b 1`n)"
            $batchContent | Out-File -FilePath $batchPath -Encoding ASCII -Force
            Write-Host "Script chromagit.bat criado" -ForegroundColor Green
        }
    }
    "3" {
        Write-Host "Removendo do PATH..." -ForegroundColor Yellow
        
        # Remover do usuário
        $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($userPath -like "*$chromaGitDir*") {
            $newUserPath = $userPath -replace [regex]::Escape($chromaGitDir + ";"), ""
            $newUserPath = $newUserPath -replace [regex]::Escape(";" + $chromaGitDir), ""
            $newUserPath = $newUserPath -replace [regex]::Escape($chromaGitDir), ""
            [Environment]::SetEnvironmentVariable("PATH", $newUserPath, "User")
            Write-Host "Removido do PATH do usuário" -ForegroundColor Green
        }
        
        # Remover do sistema se for admin
        $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
        $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
        $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
        
        if ($isAdmin) {
            $systemPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
            if ($systemPath -like "*$chromaGitDir*") {
                $newSystemPath = $systemPath -replace [regex]::Escape($chromaGitDir + ";"), ""
                $newSystemPath = $newSystemPath -replace [regex]::Escape(";" + $chromaGitDir), ""
                $newSystemPath = $newSystemPath -replace [regex]::Escape($chromaGitDir), ""
                [Environment]::SetEnvironmentVariable("PATH", $newSystemPath, "Machine")
                Write-Host "Removido do PATH do sistema" -ForegroundColor Green
            }
        }
    }
    "4" {
        Write-Host "Operação cancelada" -ForegroundColor Yellow
        exit 0
    }
    default {
        Write-Host "Opção inválida" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "Concluído!" -ForegroundColor Green
Write-Host "Reinicie o terminal para usar: chromagit" -ForegroundColor Yellow
