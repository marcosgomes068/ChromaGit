#!/usr/bin/env python3
"""
ChromaGit - Sistema de Controle de Versão Moderno

Ponto de entrada principal que integra todas as funcionalidades do ChromaGit
em uma interface unificada, limpa e poderosa.

Autor: ChromaGit Team
Versão: 1.0.0
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
import json
import time

console = Console()

class ChromaGitMain:
    def __init__(self):
        self.version = "1.0.0"
        self.name = "ChromaGit"
        self.description = "Sistema de Controle de Versão Moderno"
        
        # Diretório base do projeto
        self.base_dir = Path(__file__).parent
        
        # Se estivermos executando a partir de obj/, ajusta o caminho
        if self.base_dir.name == "obj":
            self.base_dir = self.base_dir.parent
        
        self.obj_dir = self.base_dir / "obj"
        
        # Configuração dos comandos
        self.commands = {
            'init': {
                'script': 'init.py',
                'exe': 'init.exe',
                'description': 'Inicializa um novo repositório ChromaGit',
                'color': 'green',
                'icon': '🏗️'
            },
            'add': {
                'script': 'add.py',
                'exe': 'add.exe', 
                'description': 'Adiciona arquivos ao staging para commit',
                'color': 'blue',
                'icon': '➕'
            },
            'commit': {
                'script': 'commit.py',
                'exe': 'commit.exe',
                'description': 'Cria um commit com os arquivos em staging',
                'color': 'yellow',
                'icon': '💾'
            },
            'log': {
                'script': 'log.py',
                'exe': 'log.exe',
                'description': 'Exibe histórico de commits do repositório',
                'color': 'cyan',
                'icon': '📊'
            },
            'push': {
                'script': 'push.py',
                'exe': 'push.exe',
                'description': 'Sincroniza com repositório remoto',
                'color': 'magenta',
                'icon': '🚀'
            },
            'help': {
                'script': 'help.py',
                'exe': 'help.exe',
                'description': 'Exibe ajuda detalhada dos comandos',
                'color': 'white',
                'icon': '❓'
            }
        }
    
    def show_banner(self):
        """Exibe o banner ASCII do ChromaGit"""
        banner = Text()
        banner.append("  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ███╗ █████╗  ██████╗ ██╗████████╗\n", style="bold blue")
        banner.append(" ██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝ ██║╚══██╔══╝\n", style="bold blue")
        banner.append(" ██║     ███████║██████╔╝██║   ██║██╔████╔██║███████║██║  ███╗██║   ██║   \n", style="bold cyan")
        banner.append(" ██║     ██╔══██║██╔══██╗██║   ██║██║╚██╔╝██║██╔══██║██║   ██║██║   ██║   \n", style="bold cyan")
        banner.append(" ╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╔╝██║   ██║   \n", style="bold magenta")
        banner.append("  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝   ╚═╝   \n", style="bold magenta")
        
        console.print(Panel(banner, border_style="bold blue", padding=(1, 2)))
        console.print(f"[dim]{self.description} v{self.version}[/dim]", justify="center")
        console.print()
    
    def get_repository_status(self):
        """Obtém status do repositório atual"""
        try:
            chromagit_path = Path.cwd() / '.chromagit'
            if not chromagit_path.exists():
                return {
                    'is_repo': False,
                    'message': 'Não é um repositório ChromaGit',
                    'style': 'red'
                }
            
            config_file = chromagit_path / 'config.json'
            if not config_file.exists():
                return {
                    'is_repo': True,
                    'message': 'Repositório sem configuração',
                    'style': 'yellow'
                }
            
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            staged_count = len(config.get('staged', []))
            commits_count = len(config.get('commits', []))
            remote_synced = config.get('metadata', {}).get('remote_synced', False)
            
            return {
                'is_repo': True,
                'staged': staged_count,
                'commits': commits_count,
                'remote_synced': remote_synced,
                'directory': Path.cwd().name,
                'style': 'green'
            }
            
        except Exception as e:
            return {
                'is_repo': False,
                'message': f'Erro ao ler repositório: {e}',
                'style': 'red'
            }
    
    def show_status_panel(self):
        """Exibe painel de status do repositório"""
        status = self.get_repository_status()
        
        if not status['is_repo']:
            return Panel(
                f"[red]✗[/red] {status['message']}\n"
                "[dim]Use 'python main.py init' para inicializar[/dim]",
                title="Status do Repositório",
                border_style=status['style'],
                width=50
            )
        
        if 'staged' not in status:
            return Panel(
                f"[{status['style']}]⚠[/{status['style']}] {status['message']}",
                title="Status do Repositório",
                border_style=status['style'],
                width=50
            )
        
        sync_status = "Sincronizado" if status['remote_synced'] else "Não sincronizado"
        sync_icon = "🔄" if status['remote_synced'] else "⏸️"
        
        return Panel(
            f"[green]✓[/green] Repositório ChromaGit ativo\n"
            f"[cyan]Arquivos em staging:[/cyan] {status['staged']}\n"
            f"[yellow]Total de commits:[/yellow] {status['commits']}\n"
            f"[blue]Diretório:[/blue] {status['directory']}\n"
            f"[magenta]Remoto:[/magenta] {sync_icon} {sync_status}",
            title="Status do Repositório",
            border_style="green",
            width=50
        )
    
    def show_quick_guide(self):
        """Exibe guia rápido de comandos"""
        return Panel(
            "[white]Comandos essenciais:[/white]\n"
            "[green]🏗️  python main.py init[/green] - Novo repositório\n"
            "[blue]➕  python main.py add .[/blue] - Adicionar arquivos\n" 
            "[yellow]💾  python main.py commit -m \"msg\"[/yellow] - Fazer commit\n"
            "[magenta]🚀  python main.py push[/magenta] - Sincronizar\n"
            "[cyan]📊  python main.py log[/cyan] - Ver histórico\n"
            "[white]❓  python main.py help[/white] - Ajuda detalhada\n\n"
            "[dim]Workflow: init → add → commit → push[/dim]",
            title="Guia Rápido",
            border_style="blue",
            width=50
        )
    
    def show_commands_table(self):
        """Exibe tabela completa de comandos"""
        table = Table(title="Comandos Disponíveis", show_header=True, header_style="bold white")
        table.add_column("Comando", style="bold", width=12)
        table.add_column("Descrição", width=40)
        table.add_column("Status", width=8)
        table.add_column("Modo", width=10)
        
        for cmd_name, cmd_info in self.commands.items():
            # Verifica disponibilidade de script e executável
            script_path = self.obj_dir / cmd_info['script']
            exe_path = self.obj_dir / cmd_info['exe']
            
            script_ok = script_path.exists()
            exe_ok = exe_path.exists()
            
            if script_ok and exe_ok:
                status = "[green]✓✓[/green]"
                mode = "Script+Exe"
            elif script_ok:
                status = "[yellow]✓○[/yellow]"
                mode = "Script"
            elif exe_ok:
                status = "[blue]○✓[/blue]"
                mode = "Exe"
            else:
                status = "[red]✗✗[/red]"
                mode = "N/A"
            
            table.add_row(
                f"[{cmd_info['color']}]{cmd_info['icon']} {cmd_name}[/{cmd_info['color']}]",
                cmd_info['description'],
                status,
                mode
            )
        
        return table
    
    def find_executable(self, command):
        """Encontra o melhor executável para um comando"""
        if command not in self.commands:
            return None, None
        
        cmd_info = self.commands[command]
        script_path = self.obj_dir / cmd_info['script']
        exe_path = self.obj_dir / cmd_info['exe']
        
        # Prioriza executável compilado, depois script Python
        if exe_path.exists():
            return str(exe_path), 'exe'
        elif script_path.exists():
            return str(script_path), 'script'
        else:
            return None, None
    
    def run_command(self, command, args):
        """Executa um comando ChromaGit"""
        executable, mode = self.find_executable(command)
        
        if executable is None:
            console.print(f"[red]Erro: Comando '{command}' não encontrado ou não disponível.[/red]")
            self.show_available_commands()
            return False
        
        try:
            # Prepara comando
            if mode == 'script':
                cmd_args = [sys.executable, executable] + args
            else:
                cmd_args = [executable] + args
            
            # Indicador visual
            with Progress(
                SpinnerColumn(),
                TextColumn(f"[bold {self.commands[command]['color']}]Executando {command}..."),
                console=console,
                transient=True
            ) as progress:
                progress.add_task("running", total=None)
                
                # Executa comando
                result = subprocess.run(
                    cmd_args,
                    capture_output=False,
                    text=True,
                    cwd=str(self.base_dir)
                )
            
            return result.returncode == 0
            
        except Exception as e:
            console.print(f"[red]Erro ao executar '{command}': {e}[/red]")
            return False
    
    def show_available_commands(self):
        """Mostra comandos disponíveis quando comando inválido"""
        console.print("\n[yellow]Comandos disponíveis:[/yellow]")
        for cmd_name, cmd_info in self.commands.items():
            console.print(f"  [cyan]python main.py {cmd_name}[/cyan] - {cmd_info['description']}")
        console.print("\n[dim]Use 'python main.py help [comando]' para ajuda específica[/dim]")
    
    def interactive_mode(self):
        """Modo interativo do ChromaGit"""
        self.show_banner()
        
        # Layout em colunas
        status_panel = self.show_status_panel()
        guide_panel = self.show_quick_guide()
        
        columns = Columns([status_panel, guide_panel], equal=True, expand=True)
        console.print(columns)
        console.print()
        console.print(self.show_commands_table())
        console.print()
        
        while True:
            try:
                command_input = Prompt.ask(
                    f"[bold blue]{self.name}[/bold blue]",
                    default="help",
                    show_default=False
                )
                
                # Comandos especiais
                if command_input.lower() in ['exit', 'quit', 'q']:
                    console.print("[green]Até logo! 👋[/green]")
                    break
                
                if command_input.lower() in ['clear', 'cls']:
                    console.clear()
                    self.show_banner()
                    status_panel = self.show_status_panel()
                    columns = Columns([status_panel, guide_panel], equal=True, expand=True)
                    console.print(columns)
                    console.print()
                    console.print(self.show_commands_table())
                    console.print()
                    continue
                
                if command_input.lower() == 'status':
                    self.show_banner()
                    status_panel = self.show_status_panel()
                    console.print(status_panel)
                    console.print()
                    continue
                
                # Parse comando
                parts = command_input.strip().split()
                if not parts:
                    continue
                
                command = parts[0]
                args = parts[1:] if len(parts) > 1 else []
                
                # Executa comando
                console.print()
                success = self.run_command(command, args)
                
                if success:
                    console.print(f"\n[green]✓ Comando '{command}' executado com sucesso[/green]")
                else:
                    console.print(f"\n[red]✗ Comando '{command}' falhou[/red]")
                
                console.print()
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Operação cancelada[/yellow]")
                break
            except EOFError:
                console.print("\n[green]Até logo! 👋[/green]")
                break
    
    def show_help(self):
        """Exibe ajuda geral do main.py"""
        self.show_banner()
        
        help_content = f"""
[bold]USO:[/bold]
  python main.py [comando] [argumentos...]
  python main.py --interactive

[bold]COMANDOS PRINCIPAIS:[/bold]"""
        
        for cmd_name, cmd_info in self.commands.items():
            help_content += f"\n  [bold {cmd_info['color']}]{cmd_info['icon']} {cmd_name:8}[/bold {cmd_info['color']}] {cmd_info['description']}"
        
        help_content += f"""

[bold]COMANDOS ESPECIAIS:[/bold]
  [bold green]🔄 status[/bold green]     Exibe status detalhado do repositório
  [bold blue]🖥️  interactive[/bold blue] Inicia modo interativo
  [bold white]📖 help[/bold white]       Exibe esta ajuda

[bold]OPÇÕES GLOBAIS:[/bold]
  --interactive, -i    Inicia modo interativo
  --version           Exibe versão do {self.name}
  --help, -h          Exibe esta ajuda

[bold]EXEMPLOS:[/bold]
  python main.py init --name "Meu Projeto"
  python main.py add *.py
  python main.py commit -m "Primeira versão" --stats
  python main.py push -p "projeto-v1.0"
  python main.py log --limit 5
  python main.py --interactive

[bold]ESTRUTURA DO PROJETO:[/bold]
  main.py           Ponto de entrada principal
  obj/              Scripts e executáveis dos comandos
  cli/              Interface CLI alternativa
  .chromagit/       Dados do repositório

[dim]Para ajuda específica de comandos: python main.py help [comando][/dim]
"""
        
        console.print(Panel(help_content, border_style="blue", title=f"Ajuda do {self.name}"))
    
    def main(self):
        """Função principal"""
        parser = argparse.ArgumentParser(
            description=f'{self.name} - {self.description}',
            add_help=False
        )
        parser.add_argument('command', nargs='?', help='Comando a executar')
        parser.add_argument('args', nargs='*', help='Argumentos do comando')
        parser.add_argument('--version', action='store_true', help='Exibe versão')
        parser.add_argument('--interactive', '-i', action='store_true', help='Modo interativo')
        parser.add_argument('--help', '-h', action='store_true', help='Exibe ajuda')
        
        args, unknown = parser.parse_known_args()
        
        # Adiciona argumentos desconhecidos
        if unknown:
            args.args.extend(unknown)
        
        # Tratamento de opções especiais
        if args.version:
            console.print(f"[bold blue]{self.name}[/bold blue] v{self.version}")
            console.print(f"[dim]{self.description}[/dim]")
            return
        
        if args.help:
            self.show_help()
            return
        
        # Modo interativo (quando não há comando ou --interactive)
        if args.interactive or (not args.command):
            self.interactive_mode()
            return
        
        # Comandos especiais
        if args.command == 'status':
            self.show_banner()
            console.print(self.show_status_panel())
            return
        
        # Verificar se é um comando válido
        if args.command not in self.commands:
            console.print(f"[red]Erro: Comando '{args.command}' não encontrado ou não disponível.[/red]")
            console.print()
            self.show_available_commands()
            sys.exit(1)
        
        # Execução direta de comando
        success = self.run_command(args.command, args.args)
        sys.exit(0 if success else 1)

def main():
    """Ponto de entrada"""
    try:
        chromagit = ChromaGitMain()
        chromagit.main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operação cancelada pelo usuário[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Erro inesperado: {e}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)

if __name__ == "__main__":
    main()