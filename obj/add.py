import os
import json
import shutil
import hashlib
import datetime
import argparse
import sys
import glob
import time
import stat
from pathlib import Path
from rich import print
from rich.console import Console
from rich.progress import track, Progress
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from collections import defaultdict
import mimetypes

console = Console()

CHROMAGIT_DIR = '.chromagit'
CONFIG_FILE = 'config.json'
PACKAGES_DIR = 'packages'
GITIGNORE_FILE = '.gitignore'
BACKUP_DIR = 'backup'
LOGS_DIR = 'logs'
TEMP_DIR = 'temp'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
BINARY_EXTENSIONS = {'.exe', '.dll', '.so', '.dylib', '.bin', '.zip', '.rar', '.7z', '.tar', '.gz'}
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.ico'}
VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'}
AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg'}

# Função para calcular hash de arquivo (detecção de mudanças)
def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

# Função para validar tamanho do arquivo
def is_file_too_large(file_path, max_size=MAX_FILE_SIZE):
    try:
        return file_path.stat().st_size > max_size
    except Exception:
        return False

# Função para detectar arquivos binários
def is_binary_file(file_path):
    ext = file_path.suffix.lower()
    if ext in BINARY_EXTENSIONS | IMAGE_EXTENSIONS | VIDEO_EXTENSIONS | AUDIO_EXTENSIONS:
        return True
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except Exception:
        return True

# Função para obter tipo MIME
def get_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(str(file_path))
    return mime_type or 'unknown'

# Função para criar backup antes de operações
def create_backup(config_path):
    backup_path = config_path.parent / BACKUP_DIR
    backup_path.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_path / f"config_backup_{timestamp}.json"
    shutil.copy2(config_path, backup_file)
    return backup_file

# Função para log de operações
def log_operation(operation, details, chromagit_path):
    logs_path = chromagit_path / LOGS_DIR
    logs_path.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    log_file = logs_path / f"add_operations_{datetime.date.today()}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {operation}: {details}\n")

# Função para validar permissões
def check_file_permissions(file_path):
    try:
        return os.access(file_path, os.R_OK) and os.access(file_path.parent, os.W_OK)
    except Exception:
        return False

# Função para encontrar a raiz do repositório ChromaGit
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

# Função para ler padrões do .gitignore
def read_gitignore(repo_path):
    gitignore_path = repo_path / GITIGNORE_FILE
    ignore_patterns = []
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    ignore_patterns.append(line)
    
    # Adiciona padrões padrão do ChromaGit
    default_patterns = ['.chromagit', '*.tmp', '*.temp', '__pycache__', '*.pyc']
    ignore_patterns.extend(default_patterns)
    return ignore_patterns

# Função para verificar se arquivo/pasta deve ser ignorado
def is_ignored(path, ignore_patterns):
    from fnmatch import fnmatch
    path_str = str(path)
    return any(fnmatch(path_str, pat) or fnmatch(path.name, pat) for pat in ignore_patterns)

# Função para expandir wildcards avançados
def expand_wildcards(patterns, repo_path):
    expanded_paths = set()
    for pattern in patterns:
        if '*' in pattern or '?' in pattern:
            # Suporte a glob recursivo
            matches = list(repo_path.glob(pattern))
            expanded_paths.update(matches)
        else:
            path = repo_path / pattern
            if path.exists():
                expanded_paths.add(path)
    return expanded_paths

# Função para detectar mudanças em arquivos já versionados
def detect_file_changes(file_path, config):
    rel_path = str(file_path.relative_to(Path.cwd()))
    file_hash = calculate_file_hash(file_path)
    
    # Verifica se arquivo já foi commitado
    for commit in config.get('commits', []):
        if 'files' in commit:
            for committed_file in commit['files']:
                if committed_file.get('path') == rel_path:
                    return committed_file.get('hash') != file_hash
    return True  # Arquivo novo

# Função para compressão de arquivos (opcional)
def compress_file(source, destination):
    import gzip
    with open(source, 'rb') as f_in:
        with gzip.open(f"{destination}.gz", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return f"{destination}.gz"

# Função para criar árvore de estrutura de pastas
def create_folder_tree(paths):
    tree = Tree("Arquivos/Pastas Adicionados")
    for path in sorted(paths):
        tree.add(str(path))
    return tree

# Função para estatísticas de operação
def calculate_statistics(files_added, folders_added, total_size, duration):
    stats = Table(title="Estatísticas da Operação")
    stats.add_column("Métrica", style="cyan")
    stats.add_column("Valor", style="green")
    
    stats.add_row("Arquivos adicionados", str(len(files_added)))
    stats.add_row("Pastas adicionadas", str(len(folders_added)))
    stats.add_row("Tamanho total", f"{total_size / 1024 / 1024:.2f} MB")
    stats.add_row("Tempo de execução", f"{duration:.2f} segundos")
    stats.add_row("Velocidade média", f"{(total_size / 1024 / 1024) / duration:.2f} MB/s")
    
    return stats

# Função para verificar conflitos com arquivos existentes
def check_conflicts(files, config):
    conflicts = []
    staged = set(config.get('staged', []))
    
    for file in files:
        rel_path = str(file.relative_to(Path.cwd()))
        if rel_path in staged:
            conflicts.append(rel_path)
    
    return conflicts

# Função principal para adicionar arquivos/pastas ao staging e copiar para packages
def add(paths, options=None):
    if options is None:
        options = {}
    
    start_time = time.time()
    
    # Encontra a raiz do repositório
    repo_path = find_repo_root()
    if repo_path is None:
        console.print('[red]Repositório ChromaGit não encontrado! Execute o comando init primeiro.[/red]')
        return False
    
    chromagit_path = repo_path / CHROMAGIT_DIR
    config_path = chromagit_path / CONFIG_FILE
    packages_path = chromagit_path / PACKAGES_DIR
    
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
    
    # Lê padrões do .gitignore
    ignore_patterns = read_gitignore(repo_path)
    
    # Garante que estruturas necessárias existam
    packages_path.mkdir(exist_ok=True)
    (chromagit_path / BACKUP_DIR).mkdir(exist_ok=True)
    (chromagit_path / LOGS_DIR).mkdir(exist_ok=True)
    (chromagit_path / TEMP_DIR).mkdir(exist_ok=True)
    
    # Expande wildcards
    if options.get('use_wildcards', True):
        expanded_paths = expand_wildcards(paths, repo_path)
    else:
        expanded_paths = {repo_path / path for path in paths}
    
    # Coleta arquivos e pastas válidos
    files_to_add = set()
    folders_to_add = set()
    skipped_files = []
    total_size = 0
    
    with Progress() as progress:
        task = progress.add_task("[green]Analisando arquivos...", total=len(expanded_paths))
        
        for path in expanded_paths:
            progress.update(task, advance=1)
            
            if not path.exists():
                console.print(f'[yellow]Arquivo/pasta não encontrado: {path.relative_to(repo_path)}[/yellow]')
                continue
                
            if is_ignored(path.relative_to(repo_path), ignore_patterns):
                if options.get('verbose', False):
                    console.print(f'[yellow]Ignorado: {path.relative_to(repo_path)}[/yellow]')
                continue
                
            if not check_file_permissions(path):
                console.print(f'[red]Sem permissão: {path.relative_to(repo_path)}[/red]')
                continue
            
            if path.is_dir():
                folders_to_add.add(path)
                # Adiciona arquivos da pasta recursivamente
                for file in path.rglob('*'):
                    if file.is_file() and not is_ignored(file.relative_to(repo_path), ignore_patterns):
                        if is_file_too_large(file) and not options.get('force_large_files', False):
                            skipped_files.append(f"{file.relative_to(repo_path)} (muito grande)")
                            continue
                        if is_binary_file(file) and not options.get('include_binary', False):
                            skipped_files.append(f"{file.relative_to(repo_path)} (binário)")
                            continue
                        files_to_add.add(file)
                        total_size += file.stat().st_size
            elif path.is_file():
                if is_file_too_large(path) and not options.get('force_large_files', False):
                    skipped_files.append(f"{path.relative_to(repo_path)} (muito grande)")
                    continue
                if is_binary_file(path) and not options.get('include_binary', False):
                    skipped_files.append(f"{path.relative_to(repo_path)} (binário)")
                    continue
                files_to_add.add(path)
                total_size += path.stat().st_size
    
    if not files_to_add and not folders_to_add:
        console.print('[yellow]Nenhum arquivo ou pasta válido para adicionar.[/yellow]')
        return False
    
    # Verifica conflitos
    conflicts = check_conflicts(files_to_add, config)
    if conflicts and not options.get('force_conflicts', False):
        console.print('[red]Conflitos detectados:[/red]')
        for conflict in conflicts:
            console.print(f'  - {conflict}')
        if not options.get('auto_resolve', False):
            return False
    
    # Adiciona ao staging com progresso visual
    staged = set(config.get('staged', []))
    files_added = []
    folders_added = []
    
    with Progress() as progress:
        task = progress.add_task("[green]Adicionando arquivos...", total=len(files_to_add))
        
        for file in files_to_add:
            progress.update(task, advance=1)
            rel_file = str(file.relative_to(repo_path))
            
            if rel_file in staged and not options.get('force_conflicts', False):
                continue
            
            # Calcula hash do arquivo
            file_hash = calculate_file_hash(file)
            file_info = {
                'path': rel_file,
                'hash': file_hash,
                'size': file.stat().st_size,
                'type': get_file_type(file),
                'added_at': datetime.datetime.now().isoformat(),
                'permissions': oct(file.stat().st_mode)[-3:]
            }
            
            staged.add(rel_file)
            files_added.append(file_info)
            
            # Copia arquivo para packages
            dest_file = packages_path / rel_file
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                if options.get('compress_files', False):
                    compress_file(file, dest_file)
                else:
                    shutil.copy2(file, dest_file)
                    
                # Log da operação
                log_operation("ADD_FILE", f"{rel_file} -> {dest_file}", chromagit_path)
                
            except Exception as e:
                console.print(f'[red]Erro ao copiar {file}: {e}[/red]')
                log_operation("ERROR", f"Falha ao copiar {rel_file}: {e}", chromagit_path)
    
    # Atualiza configuração
    config['staged'] = sorted(staged)
    config['last_add_operation'] = {
        'timestamp': datetime.datetime.now().isoformat(),
        'files_count': len(files_added),
        'total_size': total_size,
        'duration': time.time() - start_time
    }
    
    # Salva configuração com backup automático
    temp_config = chromagit_path / TEMP_DIR / 'config_temp.json'
    with open(temp_config, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    
    # Remove atributos de somente leitura/oculto antes de sobrescrever (Windows)
    if os.name == 'nt' and config_path.exists():
        os.system(f'attrib -r -h "{config_path}"')
    
    shutil.move(temp_config, config_path)
    
    # Restaura atributo oculto após salvar (Windows)
    if os.name == 'nt':
        os.system(f'attrib +h "{config_path}"')
    
    # Exibe resultados
    end_time = time.time()
    duration = end_time - start_time
    
    # Painel de resumo
    summary = Panel(
        f"[green]✓[/green] {len(files_added)} arquivos adicionados\n"
        f"[green]✓[/green] {len(folders_added)} pastas processadas\n"
        f"[blue]ℹ[/blue] {len(skipped_files)} arquivos ignorados\n"
        f"[yellow]⚡[/yellow] Operação concluída em {duration:.2f}s",
        title="Resumo da Operação",
        border_style="green"
    )
    console.print(summary)
    
    # Exibe arquivos ignorados se houver
    if skipped_files and options.get('verbose', False):
        console.print("\n[yellow]Arquivos ignorados:[/yellow]")
        for skipped in skipped_files[:10]:  # Limita a 10 para não poluir
            console.print(f"  - {skipped}")
        if len(skipped_files) > 10:
            console.print(f"  ... e mais {len(skipped_files) - 10} arquivos")
    
    # Exibe estatísticas detalhadas
    if options.get('show_stats', False):
        stats = calculate_statistics(files_added, folders_added, total_size, duration)
        console.print(stats)
    
    # Exibe árvore de estrutura
    if options.get('show_tree', False) and (files_added or folders_added):
        tree_paths = [info['path'] for info in files_added]
        tree = create_folder_tree(tree_paths)
        console.print(tree)
    
    log_operation("ADD_OPERATION_COMPLETE", f"Added {len(files_added)} files", chromagit_path)
    return True

# Função para linha de comando
def main():
    parser = argparse.ArgumentParser(description='Adiciona arquivos ao staging do ChromaGit')
    parser.add_argument('paths', nargs='+', help='Arquivos/pastas para adicionar')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verboso')
    parser.add_argument('-f', '--force', action='store_true', help='Força adição mesmo com conflitos')
    parser.add_argument('-b', '--binary', action='store_true', help='Inclui arquivos binários')
    parser.add_argument('-l', '--large', action='store_true', help='Inclui arquivos grandes')
    parser.add_argument('-c', '--compress', action='store_true', help='Comprime arquivos ao copiar')
    parser.add_argument('-s', '--stats', action='store_true', help='Exibe estatísticas detalhadas')
    parser.add_argument('-t', '--tree', action='store_true', help='Exibe árvore de estrutura')
    parser.add_argument('--no-wildcards', action='store_true', help='Desabilita expansão de wildcards')
    parser.add_argument('--auto-resolve', action='store_true', help='Resolve conflitos automaticamente')
    
    args = parser.parse_args()
    
    options = {
        'verbose': args.verbose,
        'force_conflicts': args.force,
        'include_binary': args.binary,
        'force_large_files': args.large,
        'compress_files': args.compress,
        'show_stats': args.stats,
        'show_tree': args.tree,
        'use_wildcards': not args.no_wildcards,
        'auto_resolve': args.auto_resolve
    }
    
    success = add(args.paths, options)
    sys.exit(0 if success else 1)

# Função para remover arquivos do staging
def remove_from_staging(paths):
    repo_path = find_repo_root()
    if repo_path is None:
        console.print('[red]Repositório ChromaGit não encontrado![/red]')
        return False
    
    chromagit_path = repo_path / CHROMAGIT_DIR
    config_path = chromagit_path / CONFIG_FILE
    
    if not config_path.exists():
        console.print('[red]Repositório não inicializado![/red]')
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    staged = set(config.get('staged', []))
    removed = []
    
    for path_str in paths:
        if path_str in staged:
            staged.remove(path_str)
            removed.append(path_str)
            console.print(f'[green]Removido do staging: {path_str}[/green]')
        else:
            console.print(f'[yellow]Não encontrado no staging: {path_str}[/yellow]')
    
    config['staged'] = sorted(staged)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    
    log_operation("REMOVE_FROM_STAGING", f"Removed {len(removed)} files", chromagit_path)
    return True

# Função para limpar staging
def clear_staging():
    repo_path = find_repo_root()
    if repo_path is None:
        console.print('[red]Repositório ChromaGit não encontrado![/red]')
        return False
    
    chromagit_path = repo_path / CHROMAGIT_DIR
    config_path = chromagit_path / CONFIG_FILE
    
    if not config_path.exists():
        console.print('[red]Repositório não inicializado![/red]')
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    count = len(config.get('staged', []))
    config['staged'] = []
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    
    console.print(f'[green]Staging limpo. {count} arquivos removidos.[/green]')
    log_operation("CLEAR_STAGING", f"Cleared {count} files", chromagit_path)
    return True

# Função para exibir status do staging
def show_status():
    repo_path = find_repo_root()
    if repo_path is None:
        console.print('[red]Repositório ChromaGit não encontrado![/red]')
        return False
    
    chromagit_path = repo_path / CHROMAGIT_DIR
    config_path = chromagit_path / CONFIG_FILE
    
    if not config_path.exists():
        console.print('[red]Repositório não inicializado![/red]')
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    staged = config.get('staged', [])
    
    if not staged:
        console.print('[yellow]Nenhum arquivo no staging.[/yellow]')
        return True
    
    table = Table(title="Arquivos no Staging")
    table.add_column("Arquivo", style="cyan")
    table.add_column("Tipo", style="green")
    table.add_column("Tamanho", style="yellow")
    
    total_size = 0
    for file_path in staged:
        full_path = repo_path / file_path
        if full_path.exists():
            size = full_path.stat().st_size
            total_size += size
            file_type = get_file_type(full_path)
            size_str = f"{size / 1024:.1f} KB" if size < 1024*1024 else f"{size / 1024 / 1024:.1f} MB"
            table.add_row(file_path, file_type, size_str)
        else:
            table.add_row(file_path, "missing", "N/A")
    
    console.print(table)
    console.print(f"\n[bold]Total: {len(staged)} arquivos, {total_size / 1024 / 1024:.2f} MB[/bold]")
    return True

# Exemplo de uso:
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()
    else:
        # Exemplo padrão
        add(['build', 'cli', 'dist', 'favicon.ico', 'LICENSE', 'main.py', 'obj', 'pyproject.toml', 'README.md', 'utils'])
