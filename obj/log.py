import os
import json
import sys
from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

CHROMAGIT_DIR = '.chromagit'
CONFIG_FILE = 'config.json'

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

def show_log(limit=10):
    """Exibe o histórico de commits do ChromaGit"""
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
    
    console.print(f"\n[bold]Histórico de Commits ({len(commits)} total)[/bold]\n")
    
    for i, commit_data in enumerate(recent_commits):
        # Formata data
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(commit_data['timestamp'])
            date_str = dt.strftime("%d/%m/%Y %H:%M:%S")
        except:
            date_str = commit_data['timestamp']
        
        # Painel do commit
        commit_panel = Panel(
            f"[yellow]Hash:[/yellow] {commit_data['hash']}\n"
            f"[blue]Autor:[/blue] {commit_data['author']['name']} <{commit_data['author']['email']}>\n"
            f"[green]Data:[/green] {date_str}\n"
            f"[cyan]Arquivos:[/cyan] {len(commit_data['files'])}\n"
            f"[magenta]Tamanho:[/magenta] {commit_data.get('stats', {}).get('total_size', 0) / 1024 / 1024:.2f} MB\n"
            f"[white]Mensagem:[/white] {commit_data['message']}",
            border_style="blue",
            title=f"Commit #{len(commits) - i}"
        )
        console.print(commit_panel)
    
    if len(commits) > limit:
        console.print(f"\n[blue]Mostrando {limit} commits mais recentes de {len(commits)} total.[/blue]")
        console.print(f"[dim]Use 'log.py --limit N' para ver mais commits.[/dim]")
    
    return True

def show_commit_details(commit_hash):
    """Exibe detalhes específicos de um commit"""
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
    
    # Procura o commit pelo hash
    target_commit = None
    for commit in commits:
        if commit['hash'].startswith(commit_hash):
            target_commit = commit
            break
    
    if target_commit is None:
        console.print(f'[red]Commit {commit_hash} não encontrado![/red]')
        return False
    
    # Exibe detalhes completos
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(target_commit['timestamp'])
        date_str = dt.strftime("%d/%m/%Y %H:%M:%S")
    except:
        date_str = target_commit['timestamp']
    
    console.print(f"\n[bold]Detalhes do Commit[/bold]\n")
    
    # Info principal
    info_panel = Panel(
        f"[yellow]Hash:[/yellow] {target_commit['hash']}\n"
        f"[blue]Autor:[/blue] {target_commit['author']['name']} <{target_commit['author']['email']}>\n"
        f"[green]Data:[/green] {date_str}\n"
        f"[cyan]Branch:[/cyan] {target_commit.get('branch', 'main')}\n"
        f"[magenta]Parent:[/magenta] {target_commit.get('parent', 'None')}\n"
        f"[white]Mensagem:[/white] {target_commit['message']}",
        title="Informações do Commit",
        border_style="green"
    )
    console.print(info_panel)
    
    # Estatísticas
    stats = target_commit.get('stats', {})
    stats_table = Table(title="Estatísticas")
    stats_table.add_column("Métrica", style="cyan")
    stats_table.add_column("Valor", style="green")
    
    stats_table.add_row("Total de Arquivos", str(stats.get('total_files', 0)))
    stats_table.add_row("Tamanho Total", f"{stats.get('total_size', 0) / 1024 / 1024:.2f} MB")
    
    # Tipos de arquivo
    file_types = stats.get('file_types', {})
    for file_type, count in file_types.items():
        stats_table.add_row(f"Arquivos {file_type or 'sem extensão'}", str(count))
    
    console.print(stats_table)
    
    # Lista de arquivos
    files_table = Table(title="Arquivos no Commit")
    files_table.add_column("Arquivo", style="cyan")
    files_table.add_column("Hash", style="green")
    files_table.add_column("Tamanho", style="yellow")
    files_table.add_column("Tipo", style="magenta")
    
    for file_info in target_commit['files']:
        size = file_info.get('size', 0)
        if size < 1024:
            size_str = f"{size} B"
        elif size < 1024 * 1024:
            size_str = f"{size / 1024:.1f} KB"
        else:
            size_str = f"{size / 1024 / 1024:.1f} MB"
        
        files_table.add_row(
            file_info['path'],
            file_info['hash'][:12] + '...',
            size_str,
            file_info.get('type', 'unknown')
        )
    
    console.print(files_table)
    
    return True

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Exibe o histórico de commits do ChromaGit')
    parser.add_argument('--limit', type=int, default=10, help='Número máximo de commits a exibir')
    parser.add_argument('--hash', help='Hash do commit para exibir detalhes específicos')
    
    args = parser.parse_args()
    
    if args.hash:
        success = show_commit_details(args.hash)
    else:
        success = show_log(args.limit)
    
    sys.exit(0 if success else 1)
