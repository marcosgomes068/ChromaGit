import argparse
import sys
from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

console = Console()

def show_general_help():
    """Exibe ajuda geral do ChromaGit"""
    
    # Título principal
    title = Text("ChromaGit - Sistema de Controle de Versão", style="bold blue")
    console.print(Panel(title, border_style="blue"))
    
    # Descrição
    description = Panel(
        "[white]ChromaGit é um sistema de controle de versão moderno e intuitivo "
        "com interface colorida e funcionalidades avançadas. Permite inicializar "
        "repositórios, fazer staging de arquivos, commits com hash único e "
        "sincronização com repositórios remotos.[/white]",
        title="Descrição",
        border_style="green"
    )
    console.print(description)
    
    # Comandos principais
    commands_table = Table(title="Comandos Principais", show_header=True, header_style="bold cyan")
    commands_table.add_column("Comando", style="cyan", width=15)
    commands_table.add_column("Descrição", style="white", width=50)
    commands_table.add_column("Exemplo", style="yellow", width=30)
    
    commands_table.add_row(
        "init", 
        "Inicializa um novo repositório ChromaGit",
        "chromagit init"
    )
    commands_table.add_row(
        "add", 
        "Adiciona arquivos ao staging para commit",
        "chromagit add arquivo.py"
    )
    commands_table.add_row(
        "commit", 
        "Cria um commit com os arquivos em staging",
        "chromagit commit -m \"Mensagem\""
    )
    commands_table.add_row(
        "log", 
        "Exibe histórico de commits",
        "chromagit log"
    )
    commands_table.add_row(
        "push", 
        "Sincroniza com repositório remoto",
        "chromagit push"
    )
    commands_table.add_row(
        "status", 
        "Mostra status do repositório",
        "chromagit status"
    )
    commands_table.add_row(
        "help", 
        "Exibe ajuda detalhada",
        "chromagit help [comando]"
    )
    
    console.print(commands_table)
    
    # Workflow básico
    workflow = Panel(
        "[yellow]1.[/yellow] [cyan]chromagit init[/cyan] - Inicializa repositório\n"
        "[yellow]2.[/yellow] [cyan]chromagit add arquivo.py[/cyan] - Adiciona arquivos\n"
        "[yellow]3.[/yellow] [cyan]chromagit commit -m \"Primeira versão\"[/cyan] - Cria commit\n"
        "[yellow]4.[/yellow] [cyan]chromagit push[/cyan] - Sincroniza com remoto\n"
        "[yellow]5.[/yellow] [cyan]chromagit log[/cyan] - Visualiza histórico",
        title="Workflow Básico",
        border_style="yellow"
    )
    console.print(workflow)
    
    # Configuração
    config_info = Panel(
        "[white]Configure o repositório remoto no arquivo [cyan].env[/cyan]:\n"
        "[green]base = \"C:\\\\Repositorios\"[/green]\n\n"
        "Para ajuda específica de um comando:\n"
        "[cyan]chromagit help [comando][/cyan]",
        title="Configuração",
        border_style="magenta"
    )
    console.print(config_info)

def show_init_help():
    """Ajuda específica para o comando init"""
    
    title = Panel("Comando: init", style="bold blue", border_style="blue")
    console.print(title)
    
    description = Panel(
        "[white]Inicializa um novo repositório ChromaGit no diretório atual. "
        "Cria a estrutura necessária (.chromagit) com configurações, logs e "
        "diretórios de backup.[/white]",
        title="Descrição",
        border_style="green"
    )
    console.print(description)
    
    # Sintaxe
    syntax = Panel(
        "[cyan]chromagit init[/cyan] [opções]",
        title="Sintaxe",
        border_style="yellow"
    )
    console.print(syntax)
    
    # Opções
    options_table = Table(title="Opções", show_header=True, header_style="bold cyan")
    options_table.add_column("Opção", style="cyan", width=20)
    options_table.add_column("Descrição", style="white", width=60)
    
    options_table.add_row("--name NOME", "Nome do repositório")
    options_table.add_row("--description DESC", "Descrição do repositório")  
    options_table.add_row("--author AUTOR", "Nome do autor padrão")
    options_table.add_row("--email EMAIL", "Email do autor padrão")
    options_table.add_row("--branch BRANCH", "Nome da branch principal (padrão: main)")
    options_table.add_row("--force", "Sobrescreve repositório existente")
    
    console.print(options_table)
    
    # Exemplos
    examples = Panel(
        "[yellow]Básico:[/yellow]\n"
        "[cyan]chromagit init[/cyan]\n\n"
        "[yellow]Com informações:[/yellow]\n"
        "[cyan]chromagit init --name \"Meu Projeto\" --author \"João Silva\"[/cyan]\n\n"
        "[yellow]Forçar criação:[/yellow]\n"
        "[cyan]chromagit init --force[/cyan]",
        title="Exemplos",
        border_style="green"
    )
    console.print(examples)

def show_add_help():
    """Ajuda específica para o comando add"""
    
    title = Panel("Comando: add", style="bold blue", border_style="blue")
    console.print(title)
    
    description = Panel(
        "[white]Adiciona arquivos ao staging para serem incluídos no próximo commit. "
        "Suporta wildcards, análise de tipos de arquivo e verificação de gitignore.[/white]",
        title="Descrição",
        border_style="green"
    )
    console.print(description)
    
    # Sintaxe
    syntax = Panel(
        "[cyan]chromagit add[/cyan] [arquivos...] [opções]",
        title="Sintaxe",
        border_style="yellow"
    )
    console.print(syntax)
    
    # Opções
    options_table = Table(title="Opções", show_header=True, header_style="bold cyan")
    options_table.add_column("Opção", style="cyan", width=25)
    options_table.add_column("Descrição", style="white", width=55)
    
    options_table.add_row("--all, -a", "Adiciona todos os arquivos modificados")
    options_table.add_row("--recursive, -r", "Busca recursivamente em diretórios")
    options_table.add_row("--include-hidden", "Inclui arquivos ocultos")
    options_table.add_row("--force, -f", "Força adição ignorando .gitignore")
    options_table.add_row("--dry-run", "Simula operação sem modificar")
    options_table.add_row("--pattern PADRÃO", "Filtra por padrão específico")
    options_table.add_row("--max-size TAMANHO", "Limite de tamanho (ex: 10MB)")
    options_table.add_row("--exclude PADRÃO", "Exclui arquivos por padrão")
    
    console.print(options_table)
    
    # Exemplos
    examples = Panel(
        "[yellow]Arquivo específico:[/yellow]\n"
        "[cyan]chromagit add arquivo.py[/cyan]\n\n"
        "[yellow]Múltiplos arquivos:[/yellow]\n"
        "[cyan]chromagit add *.py *.txt[/cyan]\n\n"
        "[yellow]Todos os arquivos:[/yellow]\n"
        "[cyan]chromagit add --all[/cyan]\n\n"
        "[yellow]Com filtro:[/yellow]\n"
        "[cyan]chromagit add --pattern \"*.py\" --max-size 1MB[/cyan]",
        title="Exemplos",
        border_style="green"
    )
    console.print(examples)

def show_commit_help():
    """Ajuda específica para o comando commit"""
    
    title = Panel("Comando: commit", style="bold blue", border_style="blue")
    console.print(title)
    
    description = Panel(
        "[white]Cria um commit permanente com os arquivos em staging. "
        "Gera hash único SHA-256, registra data/hora e autor, atualiza histórico.[/white]",
        title="Descrição",
        border_style="green"
    )
    console.print(description)
    
    # Sintaxe
    syntax = Panel(
        "[cyan]chromagit commit[/cyan] [opções]",
        title="Sintaxe",
        border_style="yellow"
    )
    console.print(syntax)
    
    # Opções
    options_table = Table(title="Opções", show_header=True, header_style="bold cyan")
    options_table.add_column("Opção", style="cyan", width=25)
    options_table.add_column("Descrição", style="white", width=55)
    
    options_table.add_row("-m, --message MSG", "Mensagem do commit")
    options_table.add_row("-a, --author AUTOR", "Nome do autor")
    options_table.add_row("-e, --email EMAIL", "Email do autor")
    options_table.add_row("-f, --force", "Força commit mesmo com arquivos ausentes")
    options_table.add_row("-i, --interactive", "Modo interativo")
    options_table.add_row("-s, --stats", "Exibe estatísticas detalhadas")
    options_table.add_row("--show-files", "Lista arquivos commitados")
    options_table.add_row("--no-interactive", "Desabilita prompts")
    
    console.print(options_table)
    
    # Exemplos
    examples = Panel(
        "[yellow]Commit básico:[/yellow]\n"
        "[cyan]chromagit commit -m \"Corrige bug crítico\"[/cyan]\n\n"
        "[yellow]Com autor:[/yellow]\n"
        "[cyan]chromagit commit -m \"Nova feature\" -a \"João\" -e \"joao@email.com\"[/cyan]\n\n"
        "[yellow]Com estatísticas:[/yellow]\n"
        "[cyan]chromagit commit -m \"Atualização\" --stats --show-files[/cyan]",
        title="Exemplos",
        border_style="green"
    )
    console.print(examples)

def show_log_help():
    """Ajuda específica para o comando log"""
    
    title = Panel("Comando: log", style="bold blue", border_style="blue")
    console.print(title)
    
    description = Panel(
        "[white]Exibe o histórico de commits do repositório com informações "
        "detalhadas incluindo hash, autor, data e arquivos modificados.[/white]",
        title="Descrição",
        border_style="green"
    )
    console.print(description)
    
    # Sintaxe
    syntax = Panel(
        "[cyan]chromagit log[/cyan] [opções]",
        title="Sintaxe",
        border_style="yellow"
    )
    console.print(syntax)
    
    # Opções
    options_table = Table(title="Opções", show_header=True, header_style="bold cyan")
    options_table.add_column("Opção", style="cyan", width=25)
    options_table.add_column("Descrição", style="white", width=55)
    
    options_table.add_row("--limit N", "Limita número de commits exibidos")
    options_table.add_row("--hash HASH", "Exibe detalhes de commit específico")
    
    console.print(options_table)
    
    # Exemplos
    examples = Panel(
        "[yellow]Histórico completo:[/yellow]\n"
        "[cyan]chromagit log[/cyan]\n\n"
        "[yellow]Últimos 5 commits:[/yellow]\n"
        "[cyan]chromagit log --limit 5[/cyan]\n\n"
        "[yellow]Commit específico:[/yellow]\n"
        "[cyan]chromagit log --hash abc123[/cyan]",
        title="Exemplos",
        border_style="green"
    )
    console.print(examples)

def show_push_help():
    """Ajuda específica para o comando push"""
    
    title = Panel("Comando: push", style="bold blue", border_style="blue")
    console.print(title)
    
    description = Panel(
        "[white]Sincroniza o repositório local com um repositório remoto. "
        "Cria subpasta no diretório base configurado no .env para organização.[/white]",
        title="Descrição",
        border_style="green"
    )
    console.print(description)
    
    # Sintaxe
    syntax = Panel(
        "[cyan]chromagit push[/cyan] [opções]",
        title="Sintaxe",
        border_style="yellow"
    )
    console.print(syntax)
    
    # Opções
    options_table = Table(title="Opções", show_header=True, header_style="bold cyan")
    options_table.add_column("Opção", style="cyan", width=25)
    options_table.add_column("Descrição", style="white", width=55)
    
    options_table.add_row("-r, --remote CAMINHO", "Caminho base remoto (sobrescreve .env)")
    options_table.add_row("-p, --project-name NOME", "Nome personalizado da subpasta")
    options_table.add_row("-f, --force", "Força push sobrescrevendo remoto")
    options_table.add_row("--no-hash", "Não verifica hash (mais rápido)")
    options_table.add_row("--status", "Exibe status do repositório remoto")
    options_table.add_row("--include-chromagit", "Inclui diretório .chromagit")
    
    console.print(options_table)
    
    # Configuração .env
    env_config = Panel(
        "[white]Configure no arquivo [cyan].env[/cyan]:\n"
        "[green]base = \"C:\\\\Repositorios\"[/green]\n\n"
        "O push criará: [yellow]C:\\Repositorios\\NomeDoProjeto\\[/yellow]",
        title="Configuração",
        border_style="magenta"
    )
    console.print(env_config)
    
    # Exemplos
    examples = Panel(
        "[yellow]Push básico:[/yellow]\n"
        "[cyan]chromagit push[/cyan]\n\n"
        "[yellow]Com nome customizado:[/yellow]\n"
        "[cyan]chromagit push -p \"MeuProjeto-v1.0\"[/cyan]\n\n"
        "[yellow]Para caminho específico:[/yellow]\n"
        "[cyan]chromagit push -r \"D:\\\\Backups\"[/cyan]\n\n"
        "[yellow]Status do remoto:[/yellow]\n"
        "[cyan]chromagit push --status[/cyan]",
        title="Exemplos",
        border_style="green"
    )
    console.print(examples)

def show_status_help():
    """Ajuda específica para o comando status"""
    
    title = Panel("Comando: status", style="bold blue", border_style="blue")
    console.print(title)
    
    description = Panel(
        "[white]Exibe o status atual do repositório incluindo arquivos em staging, "
        "commits, configurações e sincronização com remoto.[/white]",
        title="Descrição",
        border_style="green"
    )
    console.print(description)
    
    # Sintaxe
    syntax = Panel(
        "[cyan]chromagit status[/cyan] [opções]",
        title="Sintaxe",
        border_style="yellow"
    )
    console.print(syntax)
    
    # Opções
    options_table = Table(title="Opções", show_header=True, header_style="bold cyan")
    options_table.add_column("Opção", style="cyan", width=25)
    options_table.add_column("Descrição", style="white", width=55)
    
    options_table.add_row("--detailed", "Exibe informações detalhadas")
    options_table.add_row("--remote", "Inclui status do repositório remoto")
    
    console.print(options_table)

def show_config_help():
    """Ajuda sobre configuração do ChromaGit"""
    
    title = Panel("Configuração do ChromaGit", style="bold blue", border_style="blue")
    console.print(title)
    
    # Arquivo .env
    env_section = Panel(
        "[white]Crie um arquivo [cyan].env[/cyan] na raiz do projeto:\n\n"
        "[green]# Diretório base para repositórios remotos\n"
        "base = \"C:\\\\ChromaGit\"\n\n"
        "# Configurações opcionais\n"
        "author = \"Seu Nome\"\n"
        "email = \"seu@email.com\"[/green]",
        title="Arquivo .env",
        border_style="green"
    )
    console.print(env_section)
    
    # Estrutura do repositório
    structure = Panel(
        "[white].chromagit/\n"
        "├── config.json     [cyan]# Configuração principal[/cyan]\n"
        "├── backup/         [yellow]# Backups automáticos[/yellow]\n"
        "├── logs/           [blue]# Logs de operações[/blue]\n"
        "├── temp/           [magenta]# Arquivos temporários[/magenta]\n"
        "└── packages/       [green]# Gestão de pacotes[/green][/white]",
        title="Estrutura do Repositório",
        border_style="cyan"
    )
    console.print(structure)

def show_advanced_help():
    """Ajuda sobre funcionalidades avançadas"""
    
    title = Panel("Funcionalidades Avançadas", style="bold blue", border_style="blue")
    console.print(title)
    
    # Wildcards e padrões
    wildcards = Panel(
        "[white]Suporte a wildcards:\n"
        "[cyan]*.py[/cyan]          [white]# Todos os arquivos Python[/white]\n"
        "[cyan]src/**/*.js[/cyan]   [white]# JavaScript em src/ recursivamente[/white]\n"
        "[cyan]test_*.py[/cyan]     [white]# Arquivos de teste[/white]\n"
        "[cyan]docs/*[/cyan]        [white]# Arquivos em docs/[/white]",
        title="Wildcards e Padrões",
        border_style="yellow"
    )
    console.print(wildcards)
    
    # Hash e integridade
    integrity = Panel(
        "[white]Sistema de hash SHA-256:\n"
        "• Cada commit tem hash único de 16 caracteres\n"
        "• Verificação de integridade automática\n"
        "• Detecção de arquivos modificados\n"
        "• Backup automático antes de operações[/white]",
        title="Integridade e Segurança",
        border_style="red"
    )
    console.print(integrity)
    
    # Performance
    performance = Panel(
        "[white]Otimizações de performance:\n"
        "• [cyan]--no-hash[/cyan] no push para sincronização rápida\n"
        "• [cyan]--dry-run[/cyan] para simular operações\n"
        "• Compressão automática de arquivos grandes\n"
        "• Cache de metadados para operações frequentes[/white]",
        title="Performance",
        border_style="green"
    )
    console.print(performance)

def main():
    parser = argparse.ArgumentParser(description='Sistema de ajuda do ChromaGit', add_help=False)
    parser.add_argument('command', nargs='?', help='Comando específico para ajuda')
    parser.add_argument('--advanced', action='store_true', help='Exibe funcionalidades avançadas')
    parser.add_argument('--config', action='store_true', help='Exibe ajuda de configuração')
    
    args = parser.parse_args()
    
    # Mapeia comandos para funções de ajuda
    help_functions = {
        'init': show_init_help,
        'add': show_add_help,
        'commit': show_commit_help,
        'log': show_log_help,
        'push': show_push_help,
        'status': show_status_help
    }
    
    if args.advanced:
        show_advanced_help()
    elif args.config:
        show_config_help()
    elif args.command:
        command = args.command.lower()
        if command in help_functions:
            help_functions[command]()
        else:
            console.print(f'[red]Comando "{command}" não encontrado.[/red]')
            console.print(f'[white]Comandos disponíveis: {", ".join(help_functions.keys())}[/white]')
            show_general_help()
    else:
        show_general_help()

if __name__ == "__main__":
    main()
