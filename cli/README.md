# ChromaGit CLI

Uma interface de linha de comando limpa, bonita e poderosa para o sistema de controle de versão ChromaGit.

## ✨ Características

- 🎨 **Interface colorida e moderna** com Rich
- 🚀 **Modo interativo** com overview em tempo real  
- 🔧 **Integração completa** com todos os comandos ChromaGit
- 📊 **Status em tempo real** do repositório
- 💡 **Ajuda contextual** e guias rápidos
- ⚡ **Execução direta** dos comandos ou modo interativo

## 🚀 Uso Rápido

### Modo Comando Direto
```bash
# Executar comandos diretamente
python chromagit.py init
python chromagit.py add arquivo.py
python chromagit.py commit -m "Primeira versão"
python chromagit.py push

# Ou usando o script batch (Windows)
chromagit.bat init
chromagit.bat add .
chromagit.bat commit -m "Atualização"
```

### Modo Interativo
```bash
# Inicia interface interativa
python chromagit.py --interactive

# Ou simplesmente
python chromagit.py
```

## 🎯 Comandos Disponíveis

| Comando | Descrição | Exemplo |
|---------|-----------|---------|
| `init` | Inicializa repositório | `chromagit init` |
| `add` | Adiciona arquivos ao staging | `chromagit add *.py` |
| `commit` | Cria commit com staging | `chromagit commit -m "msg"` |
| `log` | Exibe histórico | `chromagit log` |
| `push` | Sincroniza com remoto | `chromagit push` |
| `help` | Ajuda detalhada | `chromagit help commit` |

## 🖥️ Interface Interativa

O modo interativo oferece:

- **Banner ASCII** colorido do ChromaGit
- **Overview do repositório** em tempo real
- **Tabela de comandos** com status
- **Guia rápido** de comandos comuns
- **Prompt inteligente** com histórico
- **Comandos especiais**:
  - `clear` ou `cls` - Limpa tela
  - `exit`, `quit` ou `q` - Sair

## 📁 Estrutura

```
cli/
├── chromagit.py      # CLI principal em Python
├── chromagit.bat     # Script runner para Windows  
└── README.md         # Esta documentação
```

## ⚙️ Requisitos

- Python 3.7+
- Biblioteca `rich` (`pip install rich`)
- Executáveis ChromaGit na pasta `../obj/`

## 🛠️ Instalação

1. **Clone o repositório ChromaGit**
2. **Instale dependências**:
   ```bash
   pip install rich
   ```
3. **Compile os executáveis** (se necessário):
   ```bash
   python -m PyInstaller --onefile obj/init.py
   python -m PyInstaller --onefile obj/add.py
   # ... outros comandos
   ```
4. **Execute a CLI**:
   ```bash
   cd cli
   python chromagit.py
   ```

## 🎨 Capturas de Tela

### Banner e Overview
```
  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ███╗ █████╗  ██████╗ ██╗████████╗
 ██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝ ██║╚══██╔══╝
 ██║     ███████║██████╔╝██║   ██║██╔████╔██║███████║██║  ███╗██║   ██║   
 ██║     ██╔══██║██╔══██╗██║   ██║██║╚██╔╝██║██╔══██║██║   ██║██║   ██║   
 ╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╔╝██║   ██║   
  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝   ╚═╝   
                    Sistema de Controle de Versão Moderno v1.0.0
```

### Tabela de Comandos
```
                                    Comandos Disponíveis                                    
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Comando    ┃ Descrição                                   ┃ Status   ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ init       │ Inicializa um novo repositório ChromaGit    │ ✓        │
│ add        │ Adiciona arquivos ao staging para commit    │ ✓        │
│ commit     │ Cria um commit com os arquivos em staging   │ ✓        │
│ log        │ Exibe histórico de commits do repositório   │ ✓        │
│ push       │ Sincroniza com repositório remoto           │ ✓        │
│ help       │ Exibe ajuda detalhada dos comandos          │ ✓        │
└────────────┴─────────────────────────────────────────────┴──────────┘
```

## 🔧 Personalização

### Modificar Cores
Edite as cores dos comandos em `chromagit.py`:
```python
self.commands = {
    'init': {'color': 'green'},    # Verde
    'add': {'color': 'blue'},      # Azul  
    'commit': {'color': 'yellow'}, # Amarelo
    # ...
}
```

### Adicionar Comandos
Para adicionar novos comandos, adicione ao dicionário `self.commands`:
```python
'status': {
    'exe': 'status.exe',
    'description': 'Exibe status do repositório',
    'color': 'cyan'
}
```

## 🐛 Solução de Problemas

### Executáveis não encontrados
- Verifique se os `.exe` estão na pasta `obj/`
- Recompile os scripts Python se necessário

### Python não encontrado
- Instale Python 3.7+ do [python.org](https://python.org)
- Adicione Python ao PATH do sistema

### Rich não instalado
```bash
pip install rich
```

### Erro de encoding (Windows)
Adicione ao início do terminal:
```cmd
chcp 65001
```

## 🎯 Roadmap

- [ ] Autocompletar comandos
- [ ] Histórico de comandos persistente  
- [ ] Configuração personalizada
- [ ] Temas de cores
- [ ] Plugins e extensões
- [ ] Modo debug/verbose
- [ ] Integração com editores

## 📝 Licença

Este projeto faz parte do ChromaGit e segue a mesma licença do projeto principal.

---

*ChromaGit CLI - Controle de versão moderno e elegante* 🚀
