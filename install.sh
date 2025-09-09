#!/bin/bash
# ChromaGit Installation Script for Linux/macOS

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "╭─────────────────────────────────────────────╮"
    echo "│           ChromaGit Installer               │"
    echo "│        Sistema de Controle de Versão        │"
    echo "╰─────────────────────────────────────────────╯"
    echo -e "${NC}"
}

print_step() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_python() {
    print_step "Verificando instalação do Python..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2)
        print_success "Python $PYTHON_VERSION encontrado"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version | cut -d ' ' -f 2)
        print_success "Python $PYTHON_VERSION encontrado"
        PYTHON_CMD="python"
    else
        print_error "Python não encontrado. Instale Python 3.8+ antes de continuar."
        exit 1
    fi
    
    # Check Python version
    PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
    PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || [ "$PYTHON_MINOR" -lt 8 ]; then
        print_error "Python 3.8+ é necessário. Versão atual: $PYTHON_VERSION"
        exit 1
    fi
}

check_pip() {
    print_step "Verificando pip..."
    
    if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
        print_error "pip não encontrado. Instale pip antes de continuar."
        exit 1
    fi
    
    print_success "pip encontrado"
}

install_dependencies() {
    print_step "Instalando dependências..."
    
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    else
        PIP_CMD="pip"
    fi
    
    $PIP_CMD install --user rich pathlib argparse hashlib || {
        print_error "Falha ao instalar dependências"
        exit 1
    }
    
    print_success "Dependências instaladas"
}

setup_chromagit() {
    print_step "Configurando ChromaGit..."
    
    # Create ChromaGit directory
    INSTALL_DIR="$HOME/.chromagit"
    
    if [ -d "$INSTALL_DIR" ]; then
        print_warning "ChromaGit já instalado em $INSTALL_DIR"
        read -p "Deseja reinstalar? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_step "Instalação cancelada"
            exit 0
        fi
        rm -rf "$INSTALL_DIR"
    fi
    
    mkdir -p "$INSTALL_DIR"
    
    # Copy files
    cp -r . "$INSTALL_DIR/"
    chmod +x "$INSTALL_DIR/main.py"
    
    print_success "ChromaGit instalado em $INSTALL_DIR"
}

create_symlink() {
    print_step "Criando link simbólico..."
    
    # Create symlink in /usr/local/bin if writable, otherwise in ~/.local/bin
    if [ -w "/usr/local/bin" ]; then
        SYMLINK_DIR="/usr/local/bin"
    else
        SYMLINK_DIR="$HOME/.local/bin"
        mkdir -p "$SYMLINK_DIR"
    fi
    
    ln -sf "$INSTALL_DIR/main.py" "$SYMLINK_DIR/chromagit"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$SYMLINK_DIR:"* ]]; then
        echo "export PATH=\"$SYMLINK_DIR:\$PATH\"" >> ~/.bashrc
        echo "export PATH=\"$SYMLINK_DIR:\$PATH\"" >> ~/.zshrc 2>/dev/null || true
        print_warning "Adicionado $SYMLINK_DIR ao PATH. Reinicie o terminal ou execute 'source ~/.bashrc'"
    fi
    
    print_success "Link simbólico criado: chromagit -> $INSTALL_DIR/main.py"
}

test_installation() {
    print_step "Testando instalação..."
    
    cd /tmp
    if $PYTHON_CMD "$INSTALL_DIR/main.py" --version &> /dev/null; then
        print_success "ChromaGit instalado e funcionando corretamente!"
    else
        print_error "Erro na instalação. ChromaGit não está funcionando."
        exit 1
    fi
}

show_usage() {
    echo -e "${GREEN}"
    echo "╭─────────────────────────────────────────────╮"
    echo "│             Instalação Concluída!           │"
    echo "╰─────────────────────────────────────────────╯"
    echo -e "${NC}"
    echo
    echo -e "${BLUE}Como usar:${NC}"
    echo "  chromagit                    # Modo interativo"
    echo "  chromagit init               # Inicializar repositório"
    echo "  chromagit add .              # Adicionar arquivos"
    echo "  chromagit commit -m \"msg\"    # Fazer commit"
    echo "  chromagit push               # Sincronizar"
    echo "  chromagit --help             # Ajuda"
    echo
    echo -e "${BLUE}Documentação:${NC}"
    echo "  $INSTALL_DIR/docs/"
    echo
    echo -e "${BLUE}Desinstalar:${NC}"
    echo "  rm -rf $INSTALL_DIR"
    echo "  rm $SYMLINK_DIR/chromagit"
}

# Main installation process
main() {
    print_header
    
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_warning "Não é recomendado executar como root"
        read -p "Continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
    
    check_python
    check_pip
    install_dependencies
    setup_chromagit
    create_symlink
    test_installation
    show_usage
    
    print_success "ChromaGit instalado com sucesso!"
}

# Run main function
main "$@"
