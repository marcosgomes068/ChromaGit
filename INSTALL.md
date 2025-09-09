# 🔧 Instalação do ChromaGit

Este documento explica como instalar o ChromaGit e adicioná-lo ao PATH do sistema para uso global.

## 📋 Índice

- [Windows](#-windows)
- [Linux/macOS](#-linuxmacos)
- [Verificação](#-verificação)
- [Desinstalação](#-desinstalação)
- [Problemas Comuns](#-problemas-comuns)

## 🪟 Windows

### Instalação Automática

1. **Execute o script PowerShell:**
   ```powershell
   PowerShell -ExecutionPolicy Bypass -File add_to_path.ps1
   ```

2. **Escolha uma opção:**
   - `1` - PATH do usuário (recomendado)
   - `2` - PATH do sistema (requer administrador)

3. **Reinicie o terminal**

### Instalação Manual

1. **Compile o executável:**
   ```powershell
   python build_simple.py
   ```

2. **Adicione ao PATH:**
   - Abra "Variáveis de Ambiente"
   - Adicione: `C:\caminho\para\ChromaGit\obj`
   - Reinicie o terminal

### Uso no Windows

```powershell
chromagit --version
chromagit init
chromagit add .
chromagit commit -m "Primeiro commit"
```

## 🐧 Linux/macOS

### Instalação Automática

1. **Execute o script bash:**
   ```bash
   chmod +x install_path.sh
   ./install_path.sh --install
   ```

2. **Recarregue o shell:**
   ```bash
   source ~/.bashrc  # ou ~/.zshrc
   ```

### Instalação Manual

1. **Crie o launcher:**
   ```bash
   mkdir -p ~/.local/bin
   ```

2. **Crie o script chromagit:**
   ```bash
   cat > ~/.local/bin/chromagit << 'EOF'
   #!/bin/bash
   cd "/caminho/para/ChromaGit"
   python3 main.py "$@"
   EOF
   ```

3. **Torne executável:**
   ```bash
   chmod +x ~/.local/bin/chromagit
   ```

4. **Adicione ao PATH:**
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

### Uso no Linux/macOS

```bash
chromagit --version
chromagit init
chromagit add .
chromagit commit -m "Primeiro commit"
```

## ✅ Verificação

### Teste a Instalação

```bash
# Verificar versão
chromagit --version

# Modo interativo
chromagit

# Ajuda
chromagit --help
```

### Saída Esperada

```
ChromaGit v1.0.0 - Sistema de Controle de Versão Moderno
```

## 🗑️ Desinstalação

### Windows

```powershell
# Usar script
PowerShell -ExecutionPolicy Bypass -File add_to_path.ps1

# Escolher opção 3 (Remover)
```

### Linux/macOS

```bash
# Usar script
./install_path.sh --remove

# Ou manual
rm ~/.local/bin/chromagit
# Remover linha do ~/.bashrc manualmente
```

## 🔧 Problemas Comuns

### Comando não encontrado

**Problema:** `chromagit: command not found`

**Soluções:**
1. Reinicie o terminal
2. Execute `source ~/.bashrc` (Linux/macOS)
3. Verifique se o PATH foi atualizado:
   ```bash
   echo $PATH | grep chromagit
   ```

### Erro de permissão

**Windows:**
- Execute como Administrador para PATH do sistema
- Use PATH do usuário (não requer admin)

**Linux/macOS:**
- Verifique permissões: `ls -la ~/.local/bin/chromagit`
- Torne executável: `chmod +x ~/.local/bin/chromagit`

### Python não encontrado

**Problema:** `Python not found`

**Soluções:**
1. Instale Python 3.7+
2. Verifique PATH do Python:
   ```bash
   python3 --version
   which python3
   ```

### Script não executa

**Windows:**
- Verifique Execution Policy:
  ```powershell
  Get-ExecutionPolicy
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

**Linux/macOS:**
- Torne o script executável:
  ```bash
  chmod +x install_path.sh
  ```

## 📁 Estrutura de Arquivos

```
ChromaGit/
├── add_to_path.ps1      # Instalador Windows
├── install_path.sh      # Instalador Linux/macOS
├── obj/
│   ├── ChromaGit.exe    # Executável Windows
│   └── chromagit.bat    # Launcher Windows
└── main.py              # Script principal
```

## 🚀 Comandos Pós-Instalação

Após a instalação bem-sucedida, você pode usar:

```bash
# Inicializar repositório
chromagit init

# Adicionar arquivos
chromagit add .
chromagit add arquivo.txt

# Fazer commit
chromagit commit -m "Mensagem do commit"

# Ver histórico
chromagit log

# Sincronizar
chromagit push

# Ajuda interativa
chromagit
```

## 🔄 Atualizações

Para atualizar o ChromaGit:

1. **Baixe a nova versão**
2. **Recompile (se necessário):**
   ```bash
   python build_simple.py
   ```
3. **Os scripts PATH não precisam ser executados novamente**

---

**💡 Dica:** Use `chromagit` sem argumentos para o modo interativo com interface colorida e intuitiva!
