#!/usr/bin/env python3
"""
ChromaGit Build System
Compila todos os módulos para executáveis standalone
"""

import subprocess
import sys
import shutil
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel

console = Console()

def build_module(module_name, progress_task=None, progress=None):
    """Compila um módulo específico para executável"""
    try:
        if progress and progress_task:
            progress.update(progress_task, description=f"Compilando {module_name}...")
        
        cmd = [
            "python", "-m", "PyInstaller",
            "--onefile",
            f"obj/{module_name}.py",
            "--distpath", "obj",
            "--workpath", "obj/build",
            "--specpath", "obj",
            "--clean"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print(f"[green]✓[/green] {module_name}.exe compilado com sucesso")
            return True
        else:
            console.print(f"[red]✗[/red] Erro ao compilar {module_name}: {result.stderr}")
            return False
            
    except Exception as e:
        console.print(f"[red]✗[/red] Erro inesperado ao compilar {module_name}: {e}")
        return False

def build_main():
    """Compila a interface principal"""
    try:
        console.print("[blue]Compilando interface principal...[/blue]")
        
        cmd = [
            "python", "-m", "PyInstaller", 
            "--onefile",
            "main.py",
            "--distpath", "obj",
            "--workpath", "obj/build", 
            "--specpath", "obj",
            "--clean",
            "--icon", "favicon.ico"  # Adiciona o favicon como ícone
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            console.print("[green]✓ main.exe compilado com sucesso[/green]")
            return True
        else:
            console.print(f"[red]✗ Erro ao compilar main.exe: {result.stderr}[/red]")
            return False
            
    except Exception as e:
        console.print(f"[red]✗ Erro inesperado ao compilar main.exe: {e}[/red]")
        return False

def clean_build_files():
    """Remove arquivos temporários de build"""
    build_dir = Path("obj/build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Remove arquivos .spec desnecessários
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
    for spec_file in Path("obj").glob("*.spec"):
        if spec_file.name != "main.spec":
            spec_file.unlink()
    
    console.print("[dim]Arquivos temporários removidos[/dim]")

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    try:
        import rich
        import PyInstaller
        return True
    except ImportError as e:
        console.print(f"[red]Dependência não encontrada: {e}[/red]")
        console.print("[yellow]Execute: pip install rich pyinstaller[/yellow]")
        return False

def main():
    """Função principal do build"""
    console.print(Panel.fit(
        "[bold blue]ChromaGit Build System[/bold blue]\n"
        "[dim]Compilando todos os módulos para produção[/dim]",
        border_style="blue"
    ))
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar se favicon existe
    favicon_path = Path("favicon.ico")
    if not favicon_path.exists():
        console.print("[yellow]⚠ favicon.ico não encontrado, usando ícone padrão[/yellow]")
    
    # Módulos para compilar
    modules = ['init', 'add', 'commit', 'log', 'push', 'help']
    
    # Progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        # Compilar módulos individuais
        task = progress.add_task("Compilando módulos...", total=len(modules))
        
        success_count = 0
        for module in modules:
            if build_module(module, task, progress):
                success_count += 1
            progress.advance(task)
        
        # Compilar interface principal
        progress.update(task, description="Compilando interface principal...")
        if build_main():
            success_count += 1
    
    # Limpar arquivos temporários
    clean_build_files()
    
    # Resumo final
    console.print()
    if success_count == len(modules) + 1:
        console.print(Panel.fit(
            f"[bold green]✓ Build concluído com sucesso![/bold green]\n"
            f"[green]{success_count}/{len(modules) + 1} executáveis compilados[/green]\n"
            f"[dim]Executáveis disponíveis em: obj/[/dim]",
            border_style="green"
        ))
    else:
        console.print(Panel.fit(
            f"[bold yellow]⚠ Build concluído com erros[/bold yellow]\n"
            f"[yellow]{success_count}/{len(modules) + 1} executáveis compilados[/yellow]\n"
            f"[dim]Verifique os erros acima[/dim]",
            border_style="yellow"
        ))
    
    # Listar executáveis criados
    console.print("\n[bold]Executáveis criados:[/bold]")
    obj_path = Path("obj")
    exe_files = list(obj_path.glob("*.exe"))
    
    if exe_files:
        for exe_file in sorted(exe_files):
            size = exe_file.stat().st_size / (1024 * 1024)  # MB
            console.print(f"  [cyan]{exe_file.name}[/cyan] - {size:.1f} MB")
    else:
        console.print("  [red]Nenhum executável encontrado[/red]")

if __name__ == "__main__":
    main()
