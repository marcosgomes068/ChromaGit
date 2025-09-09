# 🌈 ChromaGit - Sistema de Controle de Versão Moderno

![ChromaGit Banner](https://img.shields.io/badge/ChromaGit-v1.0.0-blue?style=for-the-badge&logo=git)
![Python](https://img.shields.io/badge/Python-3.13+-green?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)

> **Um sistema de controle de versão moderno e intuitivo, construído em Python com interface rica e colorida.**

## 🚀 Características

- 🎨 **Interface Rica**: Console colorido e interativo usando Rich
- 🔧 **Múltiplas Interfaces**: Script Python, executável standalone, modo interativo
- 📦 **Sistema Completo**: Init, Add, Commit, Log, Push, Help
- 🔄 **Sincronização Remota**: Push inteligente com organização automática
- 💾 **Backup Automático**: Sistema de backup integrado
- 🔐 **Hash SHA-256**: Integridade garantida dos commits
- 🌍 **Cross-Platform**: Funciona em Windows, Linux e macOS

## 📦 Instalação

### Pré-requisitos
- Python 3.13+ 
- Poetry (recomendado) ou pip

### Instalação via Poetry
```bash
git clone https://github.com/marcosgomes068/ChromaGit.git
cd ChromaGit
poetry install
```

### Instalação via pip
```bash
git clone https://github.com/marcosgomes068/ChromaGit.git
cd ChromaGit
pip install -r requirements.txt
```

### Executável Standalone
Baixe o executável `main.exe` da pasta `obj/` para usar sem instalação do Python.

## 🎯 Uso Rápido

### Modo Interativo (Recomendado)
```bash
python main.py
```

### Comandos Diretos
```bash
# Inicializar repositório
python main.py init

# Adicionar arquivos
python main.py add .

# Fazer commit
python main.py commit -m "Primeira versão"

# Sincronizar remotamente
python main.py push

# Ver histórico
python main.py log

# Status do repositório
python main.py status

# Ajuda
python main.py help
```

### Executável Standalone
```bash
# Windows
.\obj\main.exe

# Linux/macOS
./obj/main
```

## 📚 Documentação

- [📖 **Guia do Usuário**](docs/user-guide.md) - Como usar o ChromaGit
- [🔧 **Guia do Desenvolvedor**](docs/developer-guide.md) - Arquitetura e desenvolvimento
- [🎯 **Referência de Comandos**](docs/commands.md) - Lista completa de comandos
- [🚀 **Guia de Instalação**](docs/installation.md) - Instalação detalhada
- [🔄 **Sistema de Push**](docs/push-system.md) - Como funciona a sincronização

## 🏗️ Arquitetura

```
ChromaGit/
├── main.py              # 🎯 Ponto de entrada principal
├── obj/                 # 🔧 Comandos core
│   ├── init.py/.exe     # Inicialização
│   ├── add.py/.exe      # Sistema de staging
│   ├── commit.py/.exe   # Criação de commits
│   ├── log.py/.exe      # Histórico
│   ├── push.py/.exe     # Sincronização
│   └── help.py/.exe     # Ajuda
├── cli/                 # 🎨 Interface alternativa
├── docs/                # 📚 Documentação
└── .chromagit/          # 💾 Dados do repositório
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Marcos Gomes** - *Desenvolvedor Principal* - [@marcosgomes068](https://github.com/marcosgomes068)

## 🙏 Agradecimentos

- Rich - Por tornar o terminal bonito
- Python Community - Por todas as bibliotecas incríveis
- Git - Por inspirar este projeto

---

<div align="center">
  <b>ChromaGit v1.0.0</b><br>
  <sub>Feito com ❤️ e Python</sub>
</div>