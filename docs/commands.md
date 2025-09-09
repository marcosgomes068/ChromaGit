# 🎯 Referência de Comandos - ChromaGit

## Visão Geral

Esta é a referência completa de todos os comandos disponíveis no ChromaGit. Cada comando pode ser executado de múltiplas formas: modo interativo, linha de comando ou executável standalone.

## 🚀 Comandos Principais

### `init` - Inicialização

Inicializa um novo repositório ChromaGit no diretório atual.

**Sintaxe:**
```bash
python main.py init [opções]
```

**Opções:**
- `--name <nome>` - Define o nome do projeto
- `--force` - Força reinicialização se já existir
- `--author <autor>` - Define o autor padrão
- `--description <desc>` - Adiciona descrição do projeto

**Exemplos:**
```bash
# Inicialização básica
python main.py init

# Com nome específico
python main.py init --name "Meu Projeto"

# Forçar reinicialização
python main.py init --force

# Com todos os metadados
python main.py init --name "App Mobile" --author "João Silva" --description "Aplicativo móvel"
```

**Saída:**
```
✓ Repositório ChromaGit inicializado com sucesso!
📁 Projeto: Meu Projeto
👤 Autor: João Silva
📝 Configuração salva em .chromagit/config.json
```

---

### `add` - Sistema de Staging

Adiciona arquivos à área de staging para o próximo commit.

**Sintaxe:**
```bash
python main.py add <padrões> [opções]
```

**Padrões suportados:**
- `.` - Todos os arquivos do diretório atual
- `*.py` - Todos os arquivos Python
- `src/` - Todos os arquivos da pasta src
- `arquivo.txt` - Arquivo específico

**Opções:**
- `--recursive` - Inclui subdiretórios recursivamente
- `--force` - Força adição mesmo com warnings
- `--dry-run` - Mostra o que seria adicionado sem executar
- `--ignore-errors` - Ignora erros de arquivos individuais

**Exemplos:**
```bash
# Adicionar todos os arquivos
python main.py add .

# Adicionar arquivos Python
python main.py add *.py

# Adicionar pasta específica
python main.py add src/ --recursive

# Teste sem executar
python main.py add . --dry-run
```

**Saída:**
```
📁 Arquivos adicionados ao staging:
  ✓ main.py (1.2 KB)
  ✓ utils.py (0.8 KB)
  ✓ README.md (2.1 KB)

📊 Total: 3 arquivos, 4.1 KB
```

---

### `commit` - Criação de Commits

Cria um commit com os arquivos em staging.

**Sintaxe:**
```bash
python main.py commit [opções]
```

**Opções:**
- `-m <mensagem>` - Mensagem do commit
- `--author <autor>` - Sobrescreve autor padrão
- `--stats` - Inclui estatísticas detalhadas
- `--timestamp <ISO>` - Define timestamp específico
- `--interactive` - Modo interativo para mensagem

**Exemplos:**
```bash
# Commit básico
python main.py commit -m "Primeira versão"

# Com estatísticas
python main.py commit -m "Nova funcionalidade" --stats

# Autor específico
python main.py commit -m "Correção de bug" --author "Maria Santos"

# Modo interativo
python main.py commit --interactive
```

**Saída:**
```
💾 Commit criado com sucesso!
🔑 Hash: a1b2c3d4e5f6...
📝 Mensagem: Primeira versão
👤 Autor: João Silva
⏰ Data: 2025-09-09 14:30:15
📊 3 arquivos alterados (+45 -12 linhas)
```

---

### `log` - Histórico de Commits

Exibe o histórico de commits do repositório.

**Sintaxe:**
```bash
python main.py log [opções]
```

**Opções:**
- `--limit <n>` - Limita número de commits exibidos
- `--stats` - Inclui estatísticas de cada commit
- `--oneline` - Formato compacto (uma linha por commit)
- `--author <autor>` - Filtra por autor
- `--since <data>` - Commits a partir de uma data
- `--format <formato>` - Formato personalizado de saída

**Exemplos:**
```bash
# Histórico completo
python main.py log

# Últimos 5 commits
python main.py log --limit 5

# Com estatísticas
python main.py log --stats

# Formato compacto
python main.py log --oneline

# Por autor
python main.py log --author "João Silva"
```

**Saída:**
```
📊 Histórico de Commits (2 commits)

🔑 a1b2c3d4e5f6... 
📝 Primeira versão
👤 João Silva
⏰ 2025-09-09 14:30:15
📁 3 arquivos alterados

🔑 b2c3d4e5f6a7...
📝 Adicionada nova funcionalidade
👤 Maria Santos  
⏰ 2025-09-09 15:45:22
📁 2 arquivos alterados
```

---

### `push` - Sincronização Remota

Sincroniza o repositório com um local remoto.

**Sintaxe:**
```bash
python main.py push [opções]
```

**Opções:**
- `-p <projeto>` - Nome do projeto para organização
- `--force` - Força push mesmo com conflitos
- `--backup` - Cria backup antes do push
- `--dry-run` - Simula push sem executar
- `--verbose` - Saída detalhada do processo

**Configuração (.env):**
```env
REMOTE_PATH=C:\Repositorios\Remotos
# ou
REMOTE_PATH=/home/user/repositories
```

**Exemplos:**
```bash
# Push básico
python main.py push

# Com nome de projeto
python main.py push -p "website-v2"

# Push forçado
python main.py push --force

# Teste sem executar
python main.py push --dry-run
```

**Saída:**
```
🚀 Iniciando sincronização remota...
📁 Projeto: website-v2
📂 Destino: C:\Repositorios\Remotos\website-v2\
📊 3 arquivos transferidos (4.1 KB)
✓ Sincronização concluída com sucesso!
```

---

### `help` - Sistema de Ajuda

Exibe ajuda geral ou específica de comandos.

**Sintaxe:**
```bash
python main.py help [comando]
```

**Exemplos:**
```bash
# Ajuda geral
python main.py help

# Ajuda específica
python main.py help commit
python main.py help push
```

---

### `status` - Status do Repositório

Comando especial que exibe o status atual do repositório.

**Sintaxe:**
```bash
python main.py status
```

**Saída:**
```
╭──────────── Status do Repositório ─────────────╮
│ ✓ Repositório ChromaGit ativo                  │
│ Arquivos em staging: 3                         │
│ Total de commits: 15                           │
│ Diretório: MeuProjeto                          │
│ Remoto: 🔄 Sincronizado                        │
╰────────────────────────────────────────────────╯
```

## 🎮 Modo Interativo

### Iniciando o Modo Interativo
```bash
python main.py
# ou
python main.py --interactive
```

### Comandos Especiais do Modo Interativo
- `status` - Atualiza informações do repositório
- `clear` ou `cls` - Limpa a tela e reexibe interface
- `exit`, `quit` ou `q` - Sai do modo interativo

### Navegação
No modo interativo, você pode:
1. Ver status em tempo real
2. Consultar guia rápido de comandos
3. Ver tabela de disponibilidade de comandos
4. Executar qualquer comando digitando diretamente

## 🔧 Opções Globais

Disponíveis para todos os comandos:

- `--help`, `-h` - Exibe ajuda
- `--version` - Exibe versão do ChromaGit
- `--verbose` - Saída detalhada
- `--quiet` - Suprime saídas não essenciais
- `--debug` - Ativa modo debug com logs detalhados

## 📱 Executáveis Standalone

Todos os comandos estão disponíveis como executáveis independentes:

```bash
# Windows
.\obj\main.exe status
.\obj\init.exe --name "Projeto"
.\obj\commit.exe -m "Mensagem"

# Linux/macOS  
./obj/main status
./obj/init --name "Projeto"
./obj/commit -m "Mensagem"
```

## 🎯 Códigos de Saída

- `0` - Sucesso
- `1` - Erro geral
- `2` - Comando não encontrado
- `3` - Argumentos inválidos
- `4` - Repositório não inicializado
- `5` - Erro de arquivo/permissão
- `6` - Erro de rede/sincronização

## 📝 Padrões de Arquivo

### Arquivos Ignorados
O ChromaGit respeita padrões `.gitignore`:
```
# Logs
*.log
debug.log

# Dependências
node_modules/
__pycache__/
*.pyc

# Ambiente
.env
.venv/

# Sistema
.DS_Store
Thumbs.db
```

### Padrões de Globbing
- `*` - Qualquer número de caracteres
- `?` - Um caractere
- `**` - Diretórios recursivos
- `[abc]` - Qualquer dos caracteres especificados
- `{*.py,*.js}` - Múltiplos padrões

## 🔗 Integração com Scripts

### Script Bash
```bash
#!/bin/bash
# deploy.sh

echo "Fazendo commit..."
python main.py commit -m "Deploy $(date)"

echo "Sincronizando..."
python main.py push -p "production"

echo "Deploy concluído!"
```

### Script PowerShell
```powershell
# deploy.ps1

Write-Host "Fazendo commit..." -ForegroundColor Green
python main.py commit -m "Deploy $(Get-Date)"

Write-Host "Sincronizando..." -ForegroundColor Blue  
python main.py push -p "production"

Write-Host "Deploy concluído!" -ForegroundColor Green
```

### Python
```python
import subprocess
import sys

def chromagit_commit(message):
    """Wrapper para commits do ChromaGit"""
    result = subprocess.run([
        sys.executable, "main.py", "commit", 
        "-m", message
    ], capture_output=True, text=True)
    
    return result.returncode == 0
```

## 🆘 Solução de Problemas Comuns

### Comando não encontrado
```bash
Erro: Comando 'xyz' não encontrado
```
**Solução:** Verifique `python main.py help` para comandos disponíveis

### Repositório não inicializado
```bash
Erro: Este diretório não é um repositório ChromaGit
```
**Solução:** Execute `python main.py init` primeiro

### Nenhum arquivo em staging
```bash
Erro: Nenhum arquivo em staging para commit
```
**Solução:** Execute `python main.py add .` primeiro

### Erro de permissão
```bash
Erro: Permissão negada ao acessar arquivo
```
**Solução:** Verifique permissões ou execute como administrador
