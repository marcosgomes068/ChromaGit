import os
import json
import shutil
import datetime
import argparse
import sys
import hashlib
from pathlib import Path
from rich import print
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()

# Constantes compatíveis com outros módulos ChromaGit
CHROMAGIT_DIR = '.chromagit'
CONFIG_FILE = 'config.json'
PACKAGES_DIR = 'packages'
BACKUP_DIR = 'backup'
LOGS_DIR = 'logs'
TEMP_DIR = 'temp'
ENV_FILE = '.env'

# Função para carregar configurações do .env
def load_env_config(repo_path):
    """Carrega configurações do arquivo .env"""
    env_path = repo_path / ENV_FILE
    config = {}
    
    if env_path.exists():
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        config[key] = value
        except Exception as e:
            console.print(f'[yellow]Aviso: Erro ao ler .env: {e}[/yellow]')
    
    return config

# Função para log de operações
def log_operation(operation, details, chromagit_path):
    logs_path = chromagit_path / LOGS_DIR
    logs_path.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().isoformat()
    log_file = logs_path / f"push_operations_{datetime.date.today()}.log"
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
    backup_file = backup_path / f"push_backup_{timestamp}.json"
    shutil.copy2(config_path, backup_file)
    return backup_file

# Função para gerar nome da subpasta do projeto
def get_project_folder_name(repo_path):
    """Gera nome da subpasta baseado no repositório local"""
    # Tenta usar o nome do diretório do repositório
    project_name = repo_path.name
    
    # Se for um nome genérico, tenta usar informações do config
    if project_name.lower() in ['chromagit', 'repo', 'repository']:
        try:
            config_path = repo_path / CHROMAGIT_DIR / CONFIG_FILE
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Tenta usar nome do repositório do config
                repo_info = config.get('repository', {})
                if repo_info.get('name'):
                    project_name = repo_info['name']
                elif repo_info.get('description'):
                    # Usa primeira palavra da descrição
                    project_name = repo_info['description'].split()[0]
        except:
            pass
    
    # Sanitiza o nome (remove caracteres especiais)
    import re
    project_name = re.sub(r'[^\w\-_]', '_', project_name)
    
    return project_name

# Função para validar e preparar o diretório remoto
def prepare_remote_directory(base_path, project_name, force=False):
    """Prepara o diretório remoto para receber o push"""
    base_path = Path(base_path)
    remote_path = base_path / project_name
    
    # Cria diretório base se não existir
    if not base_path.exists():
        console.print(f'[blue]Criando diretório base: {base_path}[/blue]')
        base_path.mkdir(parents=True, exist_ok=True)
    
    if remote_path.exists():
        if not remote_path.is_dir():
            console.print(f'[red]Erro: {remote_path} existe mas não é um diretório![/red]')
            return False, None
        
        # Verifica se é um repositório ChromaGit
        remote_chromagit = remote_path / CHROMAGIT_DIR
        if remote_chromagit.exists():
            if not force:
                console.print(f'[yellow]Repositório ChromaGit já existe em {remote_path}[/yellow]')
                if not Confirm.ask("Sobrescrever repositório remoto?"):
                    return False, None
        
        # Backup do repositório remoto se existir
        if remote_chromagit.exists():
            backup_name = f"{project_name}_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_path = base_path / backup_name
            console.print(f'[blue]Criando backup do repositório remoto: {backup_path}[/blue]')
            shutil.copytree(remote_chromagit, backup_path / CHROMAGIT_DIR)
    else:
        # Cria o diretório do projeto remoto
        console.print(f'[blue]Criando diretório do projeto: {remote_path}[/blue]')
        remote_path.mkdir(parents=True, exist_ok=True)
    
    return True, remote_path

# Função para calcular hash de arquivo
def calculate_file_hash(file_path):
    """Calcula hash SHA-256 de um arquivo"""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

# Função para sincronizar arquivos
def sync_files(local_repo, remote_repo, options=None):
    """Sincroniza arquivos do repositório local para o remoto"""
    if options is None:
        options = {}
    
    sync_stats = {
        'copied': 0,
        'updated': 0,
        'skipped': 0,
        'errors': 0,
        'total_size': 0
    }
    
    # Lista todos os arquivos do repositório local (exceto .chromagit temporariamente)
    local_files = []
    for root, dirs, files in os.walk(local_repo):
        # Pula diretórios específicos se solicitado
        if CHROMAGIT_DIR in dirs and not options.get('include_chromagit', True):
            dirs.remove(CHROMAGIT_DIR)
        
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(local_repo)
            local_files.append(rel_path)
    
    # Progress bar para sincronização
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Sincronizando..."),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("Copiando arquivos...", total=len(local_files))
        
        for rel_path in local_files:
            progress.update(task, advance=1)
            
            local_file = local_repo / rel_path
            remote_file = remote_repo / rel_path
            
            try:
                # Cria diretório pai se necessário
                remote_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Verifica se precisa copiar/atualizar
                should_copy = True
                action = "copied"
                
                if remote_file.exists():
                    if options.get('check_hash', True):
                        local_hash = calculate_file_hash(local_file)
                        remote_hash = calculate_file_hash(remote_file)
                        
                        if local_hash == remote_hash:
                            should_copy = False
                            action = "skipped"
                        else:
                            action = "updated"
                    else:
                        # Compara por timestamp
                        local_mtime = local_file.stat().st_mtime
                        remote_mtime = remote_file.stat().st_mtime
                        
                        if local_mtime <= remote_mtime:
                            should_copy = False
                            action = "skipped"
                        else:
                            action = "updated"
                
                if should_copy:
                    # Remove atributos de somente leitura no destino (Windows)
                    if os.name == 'nt' and remote_file.exists():
                        os.system(f'attrib -r -h "{remote_file}"')
                    
                    shutil.copy2(local_file, remote_file)
                    sync_stats['total_size'] += local_file.stat().st_size
                
                sync_stats[action] += 1
                
            except Exception as e:
                console.print(f'[red]Erro ao copiar {rel_path}: {e}[/red]')
                sync_stats['errors'] += 1
    
    return sync_stats

# Função para atualizar metadados do push
def update_push_metadata(config, remote_path, sync_stats, project_name=None, base_path=None):
    """Atualiza metadados relacionados ao push"""
    if 'remote' not in config:
        config['remote'] = {}
    
    config['remote'].update({
        'path': str(remote_path),
        'base_path': str(base_path) if base_path else None,
        'project_name': project_name,
        'last_push': datetime.datetime.now().isoformat(),
        'last_push_stats': sync_stats,
        'total_pushes': config['remote'].get('total_pushes', 0) + 1
    })
    
    if 'metadata' not in config:
        config['metadata'] = {}
    
    config['metadata']['last_push'] = config['remote']['last_push']
    config['metadata']['remote_synced'] = True
    config['metadata']['remote_project_name'] = project_name
    
    return config

# Função principal para push
def push(base_remote_path=None, options=None):
    """Executa o push do repositório local para o remoto"""
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
    
    # Carrega configuração do .env se base_remote_path não fornecido
    if base_remote_path is None:
        env_config = load_env_config(repo_path)
        base_remote_path = env_config.get('base')
        
        if base_remote_path is None:
            console.print('[red]Caminho base não especificado! Configure no arquivo .env ou use --remote[/red]')
            return False
    
    # Gera nome da subpasta do projeto
    project_name = get_project_folder_name(repo_path)
    
    # Permite override do nome do projeto
    if options.get('project_name'):
        project_name = options['project_name']
    
    # Cria backup do config
    backup_file = create_backup(config_path)
    console.print(f'[blue]Backup criado: {backup_file.name}[/blue]')
    
    # Carrega configuração local
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Verifica se há commits para fazer push
    commits = config.get('commits', [])
    if not commits and not options.get('force', False):
        console.print('[yellow]Nenhum commit encontrado para push.[/yellow]')
        if not Confirm.ask("Fazer push mesmo assim?"):
            return False
    
    # Prepara diretório remoto
    success, remote_path = prepare_remote_directory(base_remote_path, project_name, options.get('force', False))
    if not success:
        return False
    
    log_operation("PUSH_STARTED", f"Remote: {remote_path}", chromagit_path)
    
    # Exibe informações do push
    info_panel = Panel(
        f"[cyan]Repositório Local:[/cyan] {repo_path}\n"
        f"[green]Diretório Base Remoto:[/green] {base_remote_path}\n"
        f"[yellow]Projeto Remoto:[/yellow] {remote_path}\n"
        f"[blue]Nome do Projeto:[/blue] {project_name}\n"
        f"[magenta]Commits a sincronizar:[/magenta] {len(commits)}\n"
        f"[white]Modo:[/white] {'Forçado' if options.get('force') else 'Normal'}",
        title="Informações do Push",
        border_style="blue"
    )
    console.print(info_panel)
    
    # Sincroniza arquivos
    console.print('\n[bold]Iniciando sincronização de arquivos...[/bold]')
    sync_stats = sync_files(repo_path, remote_path, options)
    
    # Atualiza configuração com metadados do push
    config = update_push_metadata(config, remote_path, sync_stats, project_name, base_remote_path)
    
    # Salva configuração atualizada
    temp_config = chromagit_path / TEMP_DIR / 'config_temp.json'
    temp_config.parent.mkdir(exist_ok=True)
    
    with open(temp_config, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    
    # Remove atributos de somente leitura/oculto antes de sobrescrever (Windows)
    if os.name == 'nt' and config_path.exists():
        os.system(f'attrib -r -h "{config_path}"')
    
    shutil.move(temp_config, config_path)
    
    # Restaura atributo oculto após salvar (Windows)
    if os.name == 'nt':
        os.system(f'attrib +h "{config_path}"')
    
    # Log da operação
    duration = (datetime.datetime.now() - start_time).total_seconds()
    log_operation("PUSH_COMPLETE", f"Duration: {duration:.2f}s, Files: {sync_stats['copied'] + sync_stats['updated']}", chromagit_path)
    
    # Exibe resultados
    results_table = Table(title="Resultados do Push")
    results_table.add_column("Operação", style="cyan")
    results_table.add_column("Quantidade", style="green")
    results_table.add_column("Detalhes", style="yellow")
    
    results_table.add_row("Arquivos Copiados", str(sync_stats['copied']), "Novos arquivos")
    results_table.add_row("Arquivos Atualizados", str(sync_stats['updated']), "Arquivos modificados")
    results_table.add_row("Arquivos Ignorados", str(sync_stats['skipped']), "Sem alterações")
    if sync_stats['errors'] > 0:
        results_table.add_row("Erros", str(sync_stats['errors']), "Falhas na cópia")
    
    console.print(results_table)
    
    # Painel de resumo final
    total_files = sync_stats['copied'] + sync_stats['updated']
    size_mb = sync_stats['total_size'] / 1024 / 1024
    
    summary = Panel(
        f"[green]✓[/green] Push concluído com sucesso!\n"
        f"[green]✓[/green] {total_files} arquivos sincronizados\n"
        f"[green]✓[/green] {size_mb:.2f} MB transferidos\n"
        f"[blue]ℹ[/blue] Projeto remoto: {remote_path}\n"
        f"[yellow]⚡[/yellow] Concluído em {duration:.2f}s",
        title="Push Finalizado",
        border_style="green"
    )
    console.print(summary)
    
    log_operation("PUSH_SUCCESS", f"Synced {total_files} files to {remote_path}", chromagit_path)
    return True

# Função para verificar status do remote
def status_remote(options=None):
    """Verifica o status do repositório remoto"""
    if options is None:
        options = {}
    
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
    
    remote_info = config.get('remote', {})
    
    if not remote_info:
        console.print('[yellow]Nenhum push realizado ainda.[/yellow]')
        return True
    
    # Exibe informações do remote
    remote_panel = Panel(
        f"[cyan]Caminho Base:[/cyan] {remote_info.get('base_path', 'N/A')}\n"
        f"[green]Projeto Remoto:[/green] {remote_info.get('path', 'N/A')}\n"
        f"[yellow]Nome do Projeto:[/yellow] {remote_info.get('project_name', 'N/A')}\n"
        f"[blue]Último Push:[/blue] {remote_info.get('last_push', 'N/A')}\n"
        f"[magenta]Total de Pushes:[/magenta] {remote_info.get('total_pushes', 0)}\n"
        f"[white]Status:[/white] {'Sincronizado' if config.get('metadata', {}).get('remote_synced') else 'Não sincronizado'}",
        title="Status do Repositório Remoto",
        border_style="blue"
    )
    console.print(remote_panel)
    
    # Estatísticas do último push
    last_stats = remote_info.get('last_push_stats', {})
    if last_stats:
        stats_table = Table(title="Estatísticas do Último Push")
        stats_table.add_column("Métrica", style="cyan")
        stats_table.add_column("Valor", style="green")
        
        stats_table.add_row("Arquivos Copiados", str(last_stats.get('copied', 0)))
        stats_table.add_row("Arquivos Atualizados", str(last_stats.get('updated', 0)))
        stats_table.add_row("Arquivos Ignorados", str(last_stats.get('skipped', 0)))
        stats_table.add_row("Erros", str(last_stats.get('errors', 0)))
        stats_table.add_row("Tamanho Total", f"{last_stats.get('total_size', 0) / 1024 / 1024:.2f} MB")
        
        console.print(stats_table)
    
    return True

# Função para linha de comando
def main():
    parser = argparse.ArgumentParser(description='Push do repositório ChromaGit para repositório remoto')
    parser.add_argument('-r', '--remote', help='Caminho base do repositório remoto (sobrescreve .env)')
    parser.add_argument('-p', '--project-name', help='Nome personalizado para a subpasta do projeto')
    parser.add_argument('-f', '--force', action='store_true', help='Força push sobrescrevendo repositório remoto')
    parser.add_argument('--no-hash', action='store_true', help='Não verifica hash dos arquivos (mais rápido)')
    parser.add_argument('--status', action='store_true', help='Exibe status do repositório remoto')
    parser.add_argument('--include-chromagit', action='store_true', help='Inclui diretório .chromagit no push')
    
    args = parser.parse_args()
    
    if args.status:
        success = status_remote()
    else:
        options = {
            'force': args.force,
            'check_hash': not args.no_hash,
            'include_chromagit': args.include_chromagit,
            'project_name': args.project_name
        }
        
        success = push(args.remote, options)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
