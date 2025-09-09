import os
import json
import datetime
import argparse
import sys
from pathlib import Path

try:
    from rich import print
    from rich.console import Console
    from rich.panel import Panel
except ImportError:
    print = print
    Console = object
    Panel = object

console = Console()

# Constantes compatíveis com add.py
CHROMAGIT_DIR = '.chromagit'
CONFIG_FILE = 'config.json'
PACKAGES_DIR = 'packages'
BACKUP_DIR = 'backup'
LOGS_DIR = 'logs'
TEMP_DIR = 'temp'

# Função para log de operações (compatível com add.py)
def log_operation(operation, details, chromagit_path):
    logs_path = chromagit_path / LOGS_DIR
    logs_path.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    log_file = logs_path / f"init_operations_{datetime.date.today()}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {operation}: {details}\n")

def init(path, options=None):
    if options is None:
        options = {}
    
    try:
        repo_path = Path(path)
        chromagit_path = repo_path / CHROMAGIT_DIR
        config_path = chromagit_path / CONFIG_FILE
        log_path = chromagit_path / 'log.txt'
        packages_path = chromagit_path / PACKAGES_DIR

        # Verifica se já está inicializado
        if chromagit_path.exists():
            if not options.get('force', False):
                console.print(f'[yellow]Repositório já inicializado em {chromagit_path}.[/yellow]')
                console.print('[blue]Use --force para reinicializar.[/blue]')
                return False
            else:
                console.print('[yellow]Reinicializando repositório...[/yellow]')

        # Cria estrutura principal do .chromagit
        chromagit_path.mkdir(parents=True, exist_ok=True)
        
        # Cria todas as subpastas necessárias (compatível com add.py)
        (chromagit_path / PACKAGES_DIR).mkdir(exist_ok=True)
        (chromagit_path / BACKUP_DIR).mkdir(exist_ok=True)
        (chromagit_path / LOGS_DIR).mkdir(exist_ok=True)
        (chromagit_path / TEMP_DIR).mkdir(exist_ok=True)
        
        if os.name == 'nt':
            os.system(f'attrib +h "{chromagit_path}"')
            os.system(f'attrib +h "{chromagit_path / PACKAGES_DIR}"')
            os.system(f'attrib +h "{chromagit_path / BACKUP_DIR}"')
            os.system(f'attrib +h "{chromagit_path / LOGS_DIR}"')
            os.system(f'attrib +h "{chromagit_path / TEMP_DIR}"')
        
        console.print('[green]Pasta .chromagit e estrutura criadas.[/green]')

        # Cria config.json com estrutura compatível com add.py
        config = {
            "repository": {
                "path": str(repo_path.resolve()),
                "branch": "main"
            },
            "version": "0.1.0",
            "commits": [],
            "packages": {},
            "staged": [],
            "metadata": {
                "created_at": datetime.datetime.now().isoformat(),
                "created_by": "ChromaGit Init",
                "last_modified": datetime.datetime.now().isoformat()
            },
            "settings": {
                "auto_backup": True,
                "max_file_size": 100 * 1024 * 1024,  # 100MB
                "compress_files": False,
                "ignore_binary": True
            }
        }
        
        # Salva config usando método compatível com add.py
        temp_config = chromagit_path / TEMP_DIR / 'config_temp.json'
        with open(temp_config, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        
        if config_path.exists() and os.name == 'nt':
            os.system(f'attrib -r -h "{config_path}"')
        
        temp_config.rename(config_path)
        
        if os.name == 'nt':
            os.system(f'attrib +h "{config_path}"')
        
        console.print('[green]Arquivo de configuração criado.[/green]')

        # Cria log.txt
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('Log de Commits ChromaGit\n')
            f.write(f'Repositório inicializado em: {datetime.datetime.now().isoformat()}\n')
            f.write('=' * 50 + '\n\n')
        
        if os.name == 'nt':
            os.system(f'attrib +h "{log_path}"')
        console.print('[green]Log de commits inicializado.[/green]')

        # Log da operação de inicialização
        log_operation("INIT_REPOSITORY", f"Repository initialized at {repo_path}", chromagit_path)
        log_operation("CREATE_STRUCTURE", "Created .chromagit directory structure", chromagit_path)
        log_operation("CREATE_CONFIG", "Created config.json with default settings", chromagit_path)
        
        # Painel de resumo
        if hasattr(console, 'print'):
            summary = Panel(
                f"[green]✓[/green] Repositório inicializado em: {repo_path}\n"
                f"[green]✓[/green] Estrutura ChromaGit criada\n"
                f"[green]✓[/green] Configuração padrão aplicada\n"
                f"[blue]ℹ[/blue] Pronto para usar comandos add, commit, etc.",
                title="Inicialização Concluída",
                border_style="green"
            )
            console.print(summary)
        else:
            console.print('[bold green]Repositório ChromaGit inicializado com sucesso![/bold green]')
        
        # Exibe próximos passos
        if options.get('verbose', False):
            console.print('\n[cyan]Próximos passos:[/cyan]')
            console.print('  1. Use: python obj/add.py <arquivos> para adicionar arquivos')
            console.print('  2. Use: python obj/add.py --help para ver todas as opções')
            console.print('  3. Configure .gitignore se necessário')
        
        return True
        
    except Exception as e:
        console.print(f'[red]Erro ao inicializar o repositório: {e}[/red]')
        if chromagit_path.exists():
            log_operation("INIT_ERROR", f"Initialization failed: {e}", chromagit_path)
        return False

# Função para linha de comando
def main():
    parser = argparse.ArgumentParser(description='Inicializa um repositório ChromaGit')
    parser.add_argument('path', nargs='?', default=os.getcwd(), help='Caminho para inicializar o repositório')
    parser.add_argument('-f', '--force', action='store_true', help='Força reinicialização mesmo se já existir')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verboso com informações extras')
    
    args = parser.parse_args()
    
    options = {
        'force': args.force,
        'verbose': args.verbose
    }
    
    success = init(args.path, options)
    sys.exit(0 if success else 1)

# Função para verificar se repositório está inicializado
def is_repo_initialized(path=None):
    if path is None:
        path = os.getcwd()
    
    repo_path = Path(path)
    chromagit_path = repo_path / CHROMAGIT_DIR
    config_path = chromagit_path / CONFIG_FILE
    
    return chromagit_path.exists() and config_path.exists()

# Função para obter informações do repositório
def get_repo_info(path=None):
    if path is None:
        path = os.getcwd()
    
    repo_path = Path(path)
    chromagit_path = repo_path / CHROMAGIT_DIR
    config_path = chromagit_path / CONFIG_FILE
    
    if not config_path.exists():
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception:
        return None

# Exemplo de uso:
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        # Exemplo padrão - inicializa na pasta atual
        init(os.getcwd())

