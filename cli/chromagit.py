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
import time

console = Console()

class ChromaGitCLI:
    def __init__(self):
        self.version = "1.0.0"
        self.obj_dir = Path(__file__).parent.parent / "obj"
        self.commands = {
            'init': {
                'exe': 'init.exe',
                'description': 'Inicializa um novo repositório ChromaGit',
                'color': 'green'
            },
            'add': {
                'exe': 'add.exe', 
                'description': 'Adiciona arquivos ao staging para commit',
                'color': 'blue'
            },
            'commit': {
                'exe': 'commit.exe',
                'description': 'Cria um commit com os arquivos em staging',
                'color': 'yellow'
            },
            'log': {
                'exe': 'log.exe',
                'description': 'Exibe histórico de commits do repositório',
                'color': 'cyan'
            },
            'push': {
                'exe': 'push.exe',
                'description': 'Sincroniza com repositório remoto',
                'color': 'magenta'
            },
            'help': {
                'exe': 'help.exe',
                'description': 'Exibe ajuda detalhada dos comandos',
                'color': 'white'
            }
        }
    
    def show_banner(self):
        """Exibe o banner do ChromaGit"""
        banner_text = Text()
        banner_text.append("  ██████╗██╗  ██╗██████╗  ██████╗ ███╗   ███╗ █████╗  ██████╗ ██╗████████╗\n", style="bold blue")
        banner_text.append(" ██╔════╝██║  ██║██╔══██╗██╔═══██╗████╗ ████║██╔══██╗██╔════╝ ██║╚══██╔══╝\n", style="bold blue")
        banner_text.append(" ██║     ███████║██████╔╝██║   ██║██╔████╔██║███████║██║  ███╗██║   ██║   \n", style="bold cyan")
        banner_text.append(" ██║     ██╔══██║██╔══██╗██║   ██║██║╚██╔╝██║██╔══██║██║   ██║██║   ██║   \n", style="bold cyan")
        banner_text.append(" ╚██████╗██║  ██║██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║╚██████╔╝██║   ██║   \n", style="bold magenta")
        banner_text.append("  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝   ╚═╝   \n", style="bold magenta")
        
        console.print(Panel(banner_text, border_style="bold blue", padding=(1, 2)))
        console.print(f"[dim]Sistema de Controle de Versão Moderno v{self.version}[/dim]", justify="center")
        console.print()
    
    def show_status_overview(self):
        """Exibe overview rápido do status"""
        try:
            # Verifica se está em um repositório ChromaGit
            chromagit_path = Path.cwd() / '.chromagit'
            if chromagit_path.exists():
                status_text = "[green]✓[/green] Repositório ChromaGit ativo"
                
                # Tenta obter informações básicas
                config_file = chromagit_path / 'config.json'
                if config_file.exists():
                    import json
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    staged_count = len(config.get('staged', []))
                    commits_count = len(config.get('commits', []))
                    
                    info_panel = Panel(
                        f"{status_text}\n"
                        f"[cyan]Arquivos em staging:[/cyan] {staged_count}\n"
                        f"[yellow]Total de commits:[/yellow] {commits_count}\n"
                        f"[blue]Diretório:[/blue] {Path.cwd().name}",
                        title="Status do Repositório",
                        border_style="green",
                        width=50
                    )
                else:
                    info_panel = Panel(
                        f"{status_text}\n[yellow]Configuração não encontrada[/yellow]",
                        title="Status do Repositório", 
                        border_style="yellow",
                        width=50
                    )
            else:
                info_panel = Panel(
                    "[red]✗[/red] Não é um repositório ChromaGit\n"
                    "[dim]Use 'chromagit init' para inicializar[/dim]",
                    title="Status do Repositório",
                    border_style="red",
                    width=50
                )
            
            return info_panel
            
        except Exception:
            return Panel(
                "[yellow]⚠[/yellow] Erro ao verificar status",
                title="Status do Repositório",
                border_style="yellow",
                width=50
            )
    
    def show_commands_table(self):
        """Exibe tabela de comandos disponíveis"""
        table = Table(title="Comandos Disponíveis", show_header=True, header_style="bold white")
        table.add_column("Comando", style="bold", width=12)
        table.add_column("Descrição", width=45)
        table.add_column("Status", width=10)
        
        for cmd_name, cmd_info in self.commands.items():
            exe_path = self.obj_dir / cmd_info['exe']
            status = "[green]✓[/green]" if exe_path.exists() else "[red]✗[/red]"
            
            table.add_row(
                f"[{cmd_info['color']}]{cmd_name}[/{cmd_info['color']}]",
                cmd_info['description'],
                status
            )
        
        return table
    
    def show_quick_help(self):
        """Exibe ajuda rápida"""
        help_panel = Panel(
            "[white]Comandos rápidos:[/white]\n"
            "[cyan]chromagit init[/cyan] - Novo repositório\n"
            "[blue]chromagit add .[/blue] - Adicionar tudo\n" 
            "[yellow]chromagit commit -m \"msg\"[/yellow] - Commit\n"
            "[magenta]chromagit push[/magenta] - Sincronizar\n"
            "[white]chromagit help[/white] - Ajuda detalhada\n\n"
            "[dim]Use 'chromagit [comando] --help' para opções específicas[/dim]",
            title="Guia Rápido",
            border_style="blue",
            width=50
        )
        return help_panel
    
    def run_command(self, command, args):
        """Executa um comando específico"""
        if command not in self.commands:
            console.print(f"[red]Erro: Comando '{command}' não encontrado.[/red]")
            self.show_available_commands()
            return False
        
        exe_path = self.obj_dir / self.commands[command]['exe']
        
        if not exe_path.exists():
            console.print(f"[red]Erro: Executável {exe_path} não encontrado.[/red]")
            console.print(f"[yellow]Verifique se os arquivos estão na pasta obj/[/yellow]")
            return False
        
        try:
            # Prepara comando com argumentos
            cmd_args = [str(exe_path)] + args
            
            # Exibe indicador de execução
            with Progress(
                SpinnerColumn(),
                TextColumn(f"[bold blue]Executando {command}..."),
                console=console,
                transient=True
            ) as progress:
                progress.add_task("running", total=None)
                
                # Executa o comando
                result = subprocess.run(
                    cmd_args,
                    capture_output=False,  # Permite saída colorida
                    text=True
                )
            
            return result.returncode == 0
            
        except Exception as e:
            console.print(f"[red]Erro ao executar comando: {e}[/red]")
            return False
    
    def show_available_commands(self):
        """Exibe comandos disponíveis quando comando inválido"""
        console.print("\n[yellow]Comandos disponíveis:[/yellow]")
        for cmd_name in self.commands.keys():
            console.print(f"  [cyan]chromagit {cmd_name}[/cyan]")
        console.print(f"\n[dim]Use 'chromagit help' para mais informações[/dim]")
    
    def interactive_mode(self):
        """Modo interativo do ChromaGit"""
        self.show_banner()
        
        # Layout em colunas
        status_panel = self.show_status_overview()
        help_panel = self.show_quick_help()
        
        columns = Columns([status_panel, help_panel], equal=True, expand=True)
        console.print(columns)
        
        console.print()
        console.print(self.show_commands_table())
        console.print()
        
        while True:
            try:
                # Prompt interativo
                command_input = Prompt.ask(
                    "[bold blue]ChromaGit[/bold blue]",
                    default="help",
                    show_default=False
                )
                
                if command_input.lower() in ['exit', 'quit', 'q']:
                    console.print("[green]Até logo! 👋[/green]")
                    break
                
                if command_input.lower() in ['clear', 'cls']:
                    console.clear()
                    self.show_banner()
                    console.print(columns)
                    console.print()
                    console.print(self.show_commands_table())
                    console.print()
                    continue
                
                # Parse do comando
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
    
    def main(self):
        """Função principal da CLI"""
        parser = argparse.ArgumentParser(
            description='ChromaGit - Sistema de Controle de Versão Moderno',
            add_help=False
        )
        parser.add_argument('command', nargs='?', help='Comando a executar')
        parser.add_argument('args', nargs='*', help='Argumentos do comando')
        parser.add_argument('--version', action='store_true', help='Exibe versão')
        parser.add_argument('--interactive', '-i', action='store_true', help='Modo interativo')
        parser.add_argument('--help', '-h', action='store_true', help='Exibe esta ajuda')
        
        # Parse apenas argumentos conhecidos para passar o resto para subcomandos
        args, unknown = parser.parse_known_args()
        
        # Adiciona argumentos desconhecidos aos args
        if unknown:
            args.args.extend(unknown)
        
        # Tratamento de argumentos especiais
        if args.version:
            console.print(f"[bold blue]ChromaGit[/bold blue] v{self.version}")
            console.print("[dim]Sistema de Controle de Versão Moderno[/dim]")
            return
        
        if args.help:
            self.show_banner()
            help_text = """
[bold]USO:[/bold]
  chromagit [comando] [argumentos...]
  chromagit --interactive

[bold]COMANDOS:[/bold]
  init      Inicializa um novo repositório ChromaGit
  add       Adiciona arquivos ao staging para commit  
  commit    Cria um commit com os arquivos em staging
  log       Exibe histórico de commits do repositório
  push      Sincroniza com repositório remoto
  help      Exibe ajuda detalhada dos comandos

[bold]OPÇÕES GLOBAIS:[/bold]
  --interactive, -i    Inicia modo interativo
  --version           Exibe versão do ChromaGit
  --help, -h          Exibe esta ajuda

[bold]EXEMPLOS:[/bold]
  chromagit init
  chromagit add arquivo.py
  chromagit commit -m "Primeira versão"
  chromagit push
  chromagit --interactive

[dim]Para ajuda específica: chromagit help [comando][/dim]
"""
            console.print(Panel(help_text, border_style="blue", title="Ajuda do ChromaGit"))
            return
        
        # Modo interativo
        if args.interactive or not args.command:
            self.interactive_mode()
            return
        
        # Execução de comando direto
        success = self.run_command(args.command, args.args)
        sys.exit(0 if success else 1)

def main():
    """Ponto de entrada principal"""
    try:
        cli = ChromaGitCLI()
        cli.main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operação cancelada pelo usuário[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Erro inesperado: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
