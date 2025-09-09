import os
import json
import hashlib
import datetime
import argparse
import sys
import uuid
from pathlib import Path
from rich import print
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()

# Constantes compatíveis com add.py e init.py
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
    log_file = logs_path / f"commit_operations_{datetime.date.today()}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {operation}: {details}\n")

# Função para encontrar a raiz do repositório
def find_repo_root(start_path=None):
    if start_path is None:
        start_path = Path.cwd()
    else:
        start_path = Path(start_path)
    
    current = start_path
    while current != current.parent:
        chromagit_path = current / CHROMAGIT_DIR
        if chromagit_path.exists() and chromagit_path.is_dir():
            return current
        current = current.parent
    
    return None

# Função para criar backup antes de operações
def create_backup(config_path):
    backup_path = config_path.parent / BACKUP_DIR
    backup_path.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_path / f"config_backup_{timestamp}.json"
    import shutil
    shutil.copy2(config_path, backup_file)
    return backup_file

# Função para gerar hash único do commit
def generate_commit_hash(commit_data):
    """Gera hash SHA-256 único baseado nos dados do commit"""
    commit_string = f"{commit_data['timestamp']}{commit_data['message']}{len(commit_data['files'])}"
    for file_info in commit_data['files']:
        commit_string += f"{file_info['path']}{file_info['hash']}"
    
    return hashlib.sha256(commit_string.encode()).hexdigest()[:16]

# Função para obter informações do autor
def get_author_info(options=None):
    if options is None:
        options = {}
    
    # Verifica se há configuração global
    author = options.get('author', 'Usuário ChromaGit')
    email = options.get('email', 'usuario@chromagit.local')
    
    if options.get('interactive', False):
        author = Prompt.ask("Nome do autor", default=author)
        email = Prompt.ask("Email do autor", default=email)
    
    return {
        'name': author,
        'email': email
    }

# Função para validar staging
def validate_staging(staged_files, repo_path):
    """Valida se todos os arquivos do staging ainda existem"""
    missing_files = []
    valid_files = []
    
    for file_path in staged_files:
        full_path = repo_path / file_path
        if full_path.exists():
            valid_files.append(file_path)
        else:
            missing_files.append(file_path)
    
    return valid_files, missing_files

# Função para calcular estatísticas do commit
def calculate_commit_stats(files_data):
    """Calcula estatísticas dos arquivos no commit"""
    total_size = sum(file_info.get('size', 0) for file_info in files_data)
    file_types = {}
    
    for file_info in files_data:
        file_type = file_info.get('type', 'unknown')
        file_types[file_type] = file_types.get(file_type, 0) + 1
    
    return {
        'total_files': len(files_data),
        'total_size': total_size,
        'file_types': file_types
    }

# Função para atualizar histórico de commits no log
def update_commit_log(commit_data, chromagit_path):
    """Atualiza o arquivo log.txt com informações do commit"""
    log_path = chromagit_path / 'log.txt'
    
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"Commit: {commit_data['hash']}\n")
        f.write(f"Data: {commit_data['timestamp']}\n")
        f.write(f"Autor: {commit_data['author']['name']} <{commit_data['author']['email']}>\n")
        f.write(f"Mensagem: {commit_data['message']}\n")
        f.write(f"Arquivos: {len(commit_data['files'])}\n")
        f.write(f"Tamanho: {commit_data['stats']['total_size'] / 1024 / 1024:.2f} MB\n")
        
        # Lista arquivos
        f.write("\nArquivos commitados:\n")
        for file_info in commit_data['files']:
            f.write(f"  - {file_info['path']}\n")

# Função para atualizar estado dos pacotes
def update_packages_state(config, commit_hash):
    """Atualiza o estado dos pacotes instalados com referência ao commit"""
    if 'packages' not in config:
        config['packages'] = {}
    
    # Atualiza timestamp do último commit que afetou pacotes
    config['packages']['last_commit'] = commit_hash
    config['packages']['last_update'] = datetime.datetime.now().isoformat()
    
    return config

# Função principal para fazer commit
def commit(message=None, options=None):
    if options is None:
        options = {}
    
    start_time = datetime.datetime.now()
    
    # Encontra a raiz do repositório
    repo_path = find_repo_root()
    if repo_path is None:
        console.print('[red]Repositório ChromaGit não encontrado! Execute o comando init primeiro.[/red]')
        return False
    
    chromagit_path = repo_path / CHROMAGIT_DIR
    config_path = chromagit_path / CONFIG_FILE
    
    # Validações iniciais
    if not config_path.exists():
        console.print('[red]Repositório não inicializado! Execute o comando init primeiro.[/red]')
        return False
    
    # Cria backup do config
    backup_file = create_backup(config_path)
    console.print(f'[blue]Backup criado: {backup_file}[/blue]')
    
    # Carrega configuração
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    staged_files = config.get('staged', [])
    
    # Verifica se há arquivos no staging
    if not staged_files:
        console.print('[yellow]Nenhum arquivo no staging para commit.[/yellow]')
        console.print('[blue]Use o comando add para adicionar arquivos primeiro.[/blue]')
        return False
    
    # Valida arquivos do staging
    valid_files, missing_files = validate_staging(staged_files, repo_path)
    
    if missing_files:
        console.print('[red]Arquivos removidos desde o último add:[/red]')
        for missing in missing_files:
            console.print(f'  - {missing}')
        
        if not options.get('force', False):
            if not Confirm.ask("Continuar mesmo assim?"):
                return False
    
    # Solicita mensagem do commit se não fornecida
    if message is None:
        if options.get('interactive', True):
            message = Prompt.ask("Mensagem do commit", default="Commit automático")
        else:
            message = "Commit automático"
    
    # Obter informações do autor
    author_info = get_author_info(options)
    
    # Coleta informações detalhadas dos arquivos
    files_data = []
    
    with Progress() as progress:
        task = progress.add_task("[green]Processando arquivos...", total=len(valid_files))
        
        for file_path in valid_files:
            progress.update(task, advance=1)
            
            full_path = repo_path / file_path
            
            # Calcula hash do arquivo
            file_hash = None
            try:
                sha256_hash = hashlib.sha256()
                with open(full_path, "rb") as f:
                    for byte_block in iter(lambda: f.read(4096), b""):
                        sha256_hash.update(byte_block)
                file_hash = sha256_hash.hexdigest()
            except Exception as e:
                console.print(f'[yellow]Erro ao calcular hash de {file_path}: {e}[/yellow]')
                file_hash = "error"
            
            # Coleta metadados do arquivo
            file_info = {
                'path': file_path,
                'hash': file_hash,
                'size': full_path.stat().st_size if full_path.exists() else 0,
                'type': full_path.suffix.lower() if full_path.exists() else 'unknown',
                'modified_time': full_path.stat().st_mtime if full_path.exists() else 0
            }
            
            files_data.append(file_info)
    
    # Cria dados do commit
    commit_data = {
        'message': message,
        'timestamp': start_time.isoformat(),
        'author': author_info,
        'files': files_data,
        'parent': config.get('commits', [])[-1]['hash'] if config.get('commits') else None,
        'branch': config.get('repository', {}).get('branch', 'main')
    }
    
    # Gera hash único do commit
    commit_data['hash'] = generate_commit_hash(commit_data)
    
    # Calcula estatísticas
    commit_data['stats'] = calculate_commit_stats(files_data)
    
    # Atualiza configuração
    if 'commits' not in config:
        config['commits'] = []
    
    config['commits'].append(commit_data)
    config['staged'] = []  # Limpa staging após commit
    
    # Atualiza estado dos pacotes
    config = update_packages_state(config, commit_data['hash'])
    
    # Atualiza metadados
    if 'metadata' not in config:
        config['metadata'] = {}
    
    config['metadata']['last_commit'] = commit_data['hash']
    config['metadata']['last_commit_time'] = commit_data['timestamp']
    config['metadata']['total_commits'] = len(config['commits'])
    config['metadata']['last_modified'] = datetime.datetime.now().isoformat()
    
    # Salva configuração
    temp_config = chromagit_path / TEMP_DIR / 'config_temp.json'
    with open(temp_config, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    
    # Remove atributos de somente leitura/oculto antes de sobrescrever (Windows)
    if os.name == 'nt' and config_path.exists():
        os.system(f'attrib -r -h "{config_path}"')
    
    import shutil
    shutil.move(temp_config, config_path)
    
    # Restaura atributo oculto após salvar (Windows)
    if os.name == 'nt':
        os.system(f'attrib +h "{config_path}"')
    
    # Atualiza log de commits
    update_commit_log(commit_data, chromagit_path)
    
    # Log da operação
    log_operation("COMMIT_CREATED", f"Hash: {commit_data['hash']}, Files: {len(files_data)}", chromagit_path)
    
    # Exibe resultados
    duration = (datetime.datetime.now() - start_time).total_seconds()
    
    # Painel de resumo
    summary = Panel(
        f"[green]✓[/green] Commit criado: {commit_data['hash']}\n"
        f"[green]✓[/green] {len(files_data)} arquivos commitados\n"
        f"[green]✓[/green] Tamanho total: {commit_data['stats']['total_size'] / 1024 / 1024:.2f} MB\n"
        f"[blue]ℹ[/blue] Autor: {author_info['name']}\n"
        f"[yellow]⚡[/yellow] Concluído em {duration:.2f}s",
        title=f"Commit: {message[:50]}{'...' if len(message) > 50 else ''}",
        border_style="green"
    )
    console.print(summary)
    
    # Exibe estatísticas detalhadas se solicitado
    if options.get('show_stats', False):
        stats_table = Table(title="Estatísticas do Commit")
        stats_table.add_column("Tipo de Arquivo", style="cyan")
        stats_table.add_column("Quantidade", style="green")
        
        for file_type, count in commit_data['stats']['file_types'].items():
            stats_table.add_row(file_type or 'sem extensão', str(count))
        
        console.print(stats_table)
    
    # Exibe arquivos commitados se solicitado
    if options.get('show_files', False):
        files_table = Table(title="Arquivos Commitados")
        files_table.add_column("Arquivo", style="cyan")
        files_table.add_column("Hash", style="green")
        files_table.add_column("Tamanho", style="yellow")
        
        for file_info in files_data[:10]:  # Limita a 10 para não poluir
            size_str = f"{file_info['size'] / 1024:.1f} KB" if file_info['size'] < 1024*1024 else f"{file_info['size'] / 1024 / 1024:.1f} MB"
            files_table.add_row(
                file_info['path'], 
                file_info['hash'][:8] + '...', 
                size_str
            )
        
        if len(files_data) > 10:
            files_table.add_row("...", f"... e mais {len(files_data) - 10} arquivos", "...")
        
        console.print(files_table)
    
    log_operation("COMMIT_COMPLETE", f"Successfully committed {len(files_data)} files", chromagit_path)
    return True

# Função para linha de comando
def main():
    parser = argparse.ArgumentParser(description='Faz commit das alterações no staging do ChromaGit')
    parser.add_argument('-m', '--message', help='Mensagem do commit')
    parser.add_argument('-a', '--author', help='Nome do autor do commit')
    parser.add_argument('-e', '--email', help='Email do autor do commit')
    parser.add_argument('-f', '--force', action='store_true', help='Força commit mesmo com arquivos ausentes')
    parser.add_argument('-i', '--interactive', action='store_true', help='Modo interativo para solicitar informações')
    parser.add_argument('-s', '--stats', action='store_true', help='Exibe estatísticas detalhadas')
    parser.add_argument('--show-files', action='store_true', help='Exibe lista de arquivos commitados')
    parser.add_argument('--no-interactive', action='store_true', help='Desabilita prompts interativos')
    
    args = parser.parse_args()
    
    options = {
        'author': args.author,
        'email': args.email,
        'force': args.force,
        'interactive': args.interactive and not args.no_interactive,
        'show_stats': args.stats,
        'show_files': args.show_files
    }
    
    success = commit(args.message, options)
    sys.exit(0 if success else 1)

# Função para exibir histórico de commits
def show_log(limit=10):
    repo_path = find_repo_root()
    if repo_path is None:
        console.print('[red]Repositório ChromaGit não encontrado![/red]')
        return False
    
    config_path = repo_path / CHROMAGIT_DIR / CONFIG_FILE
    
    if not config_path.exists():
        console.print('[red]Repositório não inicializado![/red]')
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    commits = config.get('commits', [])
    
    if not commits:
        console.print('[yellow]Nenhum commit encontrado.[/yellow]')
        return True
    
    # Exibe commits mais recentes primeiro
    recent_commits = commits[-limit:] if len(commits) > limit else commits
    recent_commits.reverse()
    
    for commit_data in recent_commits:
        commit_panel = Panel(
            f"[yellow]Hash:[/yellow] {commit_data['hash']}\n"
            f"[blue]Autor:[/blue] {commit_data['author']['name']} <{commit_data['author']['email']}>\n"
            f"[green]Data:[/green] {commit_data['timestamp']}\n"
            f"[cyan]Arquivos:[/cyan] {len(commit_data['files'])}\n"
            f"[white]Mensagem:[/white] {commit_data['message']}",
            border_style="blue"
        )
        console.print(commit_panel)
    
    if len(commits) > limit:
        console.print(f"\n[blue]Mostrando {limit} commits mais recentes de {len(commits)} total.[/blue]")
    
    return True

# Exemplo de uso:
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        # Exemplo padrão
        commit("Commit automático via script")
