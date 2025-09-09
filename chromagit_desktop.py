#!/usr/bin/env python3
"""
ChromaGit Desktop App
Aplicação desktop unificada do ChromaGit com interface rica
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import subprocess
import json
import threading
from datetime import datetime

# Adicionar diretório do projeto ao path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

class ChromaGitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChromaGit - Sistema de Controle de Versão")
        self.root.geometry("900x700")
        
        # Configurar ícone se favicon existir
        favicon_path = project_dir / "favicon.ico"
        if favicon_path.exists():
            try:
                self.root.iconbitmap(str(favicon_path))
            except:
                pass  # Ignora se não conseguir carregar o ícone
        
        self.current_dir = Path.cwd()
        self.setup_ui()
        self.refresh_status()
    
    def setup_ui(self):
        """Configura a interface do usuário"""
        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Abrir Pasta", command=self.open_folder)
        file_menu.add_command(label="Atualizar", command=self.refresh_status)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Repositório
        repo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Repositório", menu=repo_menu)
        repo_menu.add_command(label="Inicializar", command=self.init_repo)
        repo_menu.add_command(label="Status", command=self.show_status)
        repo_menu.add_separator()
        repo_menu.add_command(label="Fazer Push", command=self.push_repo)
        
        # Menu Ajuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)
        help_menu.add_command(label="Documentação", command=self.show_docs)
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="🌈 ChromaGit", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0)
        
        self.current_dir_label = ttk.Label(header_frame, text=f"📁 {self.current_dir}")
        self.current_dir_label.grid(row=1, column=0, sticky=tk.W)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status do Repositório", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        self.status_text = tk.Text(status_frame, height=6, wrap=tk.WORD)
        status_scroll = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scroll.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botões principais
        ttk.Button(controls_frame, text="🏗️ Inicializar", 
                  command=self.init_repo).grid(row=0, column=0, padx=5)
        ttk.Button(controls_frame, text="➕ Adicionar Tudo", 
                  command=self.add_all).grid(row=0, column=1, padx=5)
        ttk.Button(controls_frame, text="💾 Fazer Commit", 
                  command=self.commit_dialog).grid(row=0, column=2, padx=5)
        ttk.Button(controls_frame, text="🚀 Push", 
                  command=self.push_repo).grid(row=0, column=3, padx=5)
        ttk.Button(controls_frame, text="📊 Log", 
                  command=self.show_log).grid(row=0, column=4, padx=5)
        ttk.Button(controls_frame, text="🔄 Atualizar", 
                  command=self.refresh_status).grid(row=0, column=5, padx=5)
        
        # Campo de mensagem de commit
        commit_frame = ttk.Frame(main_frame)
        commit_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        commit_frame.columnconfigure(1, weight=1)
        
        ttk.Label(commit_frame, text="Mensagem do Commit:").grid(row=0, column=0, sticky=tk.W)
        self.commit_message = ttk.Entry(commit_frame, width=50)
        self.commit_message.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Output
        output_frame = ttk.LabelFrame(main_frame, text="Saída de Comandos", padding="10")
        output_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = tk.Text(output_frame, wrap=tk.WORD)
        output_scroll = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=output_scroll.set)
        
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def log_output(self, message, level="INFO"):
        """Adiciona mensagem ao log de saída"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        self.output_text.insert(tk.END, formatted_message)
        self.output_text.see(tk.END)
        self.root.update()
    
    def run_chromagit_command(self, command, *args):
        """Executa um comando do ChromaGit"""
        try:
            cmd = [sys.executable, str(project_dir / "main.py"), command] + list(args)
            self.log_output(f"Executando: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  cwd=str(self.current_dir))
            
            if result.stdout:
                self.log_output(result.stdout.strip())
            
            if result.stderr:
                self.log_output(result.stderr.strip(), "ERROR")
            
            if result.returncode == 0:
                self.log_output("Comando executado com sucesso!", "SUCCESS")
            else:
                self.log_output(f"Comando falhou com código {result.returncode}", "ERROR")
            
            return result.returncode == 0
            
        except Exception as e:
            self.log_output(f"Erro ao executar comando: {e}", "ERROR")
            return False
    
    def refresh_status(self):
        """Atualiza o status do repositório"""
        self.log_output("Atualizando status...")
        
        # Verificar se é um repositório ChromaGit
        chromagit_dir = self.current_dir / ".chromagit"
        
        status_info = []
        
        if chromagit_dir.exists():
            status_info.append("✅ Repositório ChromaGit ativo")
            
            # Ler configuração
            config_file = chromagit_dir / "config.json"
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    status_info.append(f"📋 Projeto: {config.get('name', 'Sem nome')}")
                    status_info.append(f"👤 Autor: {config.get('author', 'Não definido')}")
                except:
                    status_info.append("⚠️ Erro ao ler configuração")
            
            # Verificar staging
            staging_file = chromagit_dir / "staging.json"
            if staging_file.exists():
                try:
                    with open(staging_file, 'r', encoding='utf-8') as f:
                        staging = json.load(f)
                    file_count = len(staging.get('files', []))
                    status_info.append(f"📝 Arquivos em staging: {file_count}")
                except:
                    status_info.append("📝 Arquivos em staging: 0")
            else:
                status_info.append("📝 Arquivos em staging: 0")
            
            # Verificar commits
            commits_file = chromagit_dir / "commits.json" 
            if commits_file.exists():
                try:
                    with open(commits_file, 'r', encoding='utf-8') as f:
                        commits_data = json.load(f)
                    commit_count = len(commits_data.get('commits', []))
                    status_info.append(f"📊 Total de commits: {commit_count}")
                except:
                    status_info.append("📊 Total de commits: 0")
            else:
                status_info.append("📊 Total de commits: 0")
        else:
            status_info.append("❌ Não é um repositório ChromaGit")
            status_info.append("💡 Use 'Inicializar' para criar um novo repositório")
        
        # Atualizar interface
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(tk.END, "\n".join(status_info))
        
        self.current_dir_label.config(text=f"📁 {self.current_dir}")
    
    def open_folder(self):
        """Abre uma pasta diferente"""
        folder = filedialog.askdirectory(initialdir=str(self.current_dir))
        if folder:
            self.current_dir = Path(folder)
            os.chdir(str(self.current_dir))
            self.log_output(f"Mudado para: {self.current_dir}")
            self.refresh_status()
    
    def init_repo(self):
        """Inicializa um repositório"""
        # Dialog para nome do projeto
        name = tk.simpledialog.askstring("Inicializar Repositório", 
                                        "Nome do projeto:")
        if name:
            threading.Thread(
                target=lambda: self.run_chromagit_command("init", "--name", name)
            ).start()
            self.root.after(1000, self.refresh_status)
    
    def add_all(self):
        """Adiciona todos os arquivos"""
        threading.Thread(
            target=lambda: self.run_chromagit_command("add", ".")
        ).start()
        self.root.after(1000, self.refresh_status)
    
    def commit_dialog(self):
        """Dialog para fazer commit"""
        message = self.commit_message.get().strip()
        if not message:
            messagebox.showwarning("Aviso", "Por favor, insira uma mensagem de commit")
            return
        
        threading.Thread(
            target=lambda: self.run_chromagit_command("commit", "-m", message)
        ).start()
        
        # Limpar campo de mensagem
        self.commit_message.delete(0, tk.END)
        self.root.after(1000, self.refresh_status)
    
    def push_repo(self):
        """Faz push do repositório"""
        threading.Thread(
            target=lambda: self.run_chromagit_command("push")
        ).start()
        self.root.after(1000, self.refresh_status)
    
    def show_log(self):
        """Mostra o log de commits"""
        threading.Thread(
            target=lambda: self.run_chromagit_command("log", "--limit", "10")
        ).start()
    
    def show_status(self):
        """Mostra status detalhado"""
        threading.Thread(
            target=lambda: self.run_chromagit_command("status")
        ).start()
    
    def show_about(self):
        """Mostra informações sobre o ChromaGit"""
        about_text = """
🌈 ChromaGit Desktop v1.0.0

Sistema de Controle de Versão Moderno
Desenvolvido em Python com interface rica

Características:
• Interface gráfica intuitiva
• Sistema de commits com hash SHA-256
• Sincronização remota automática
• Backup integrado
• Multiplataforma

Desenvolvido por: Marcos Gomes
GitHub: @marcosgomes068

Licença: MIT
        """
        messagebox.showinfo("Sobre ChromaGit", about_text.strip())
    
    def show_docs(self):
        """Abre a documentação"""
        docs_path = project_dir / "docs"
        if docs_path.exists():
            try:
                if sys.platform == "win32":
                    os.startfile(str(docs_path))
                elif sys.platform == "darwin":
                    subprocess.run(["open", str(docs_path)])
                else:
                    subprocess.run(["xdg-open", str(docs_path)])
            except:
                messagebox.showinfo("Documentação", 
                                  f"Documentação disponível em:\n{docs_path}")
        else:
            messagebox.showwarning("Aviso", "Documentação não encontrada")

def main():
    """Função principal da aplicação"""
    # Verificar se tkinter está disponível
    try:
        import tkinter.simpledialog
    except ImportError:
        print("ERRO: tkinter não está disponível")
        print("No Ubuntu/Debian: sudo apt-get install python3-tk")
        print("No CentOS/RHEL: sudo yum install tkinter")
        sys.exit(1)
    
    # Criar e executar aplicação
    root = tk.Tk()
    app = ChromaGitApp(root)
    
    # Configurar fechamento
    def on_closing():
        app.log_output("Fechando ChromaGit Desktop...")
        root.quit()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        on_closing()

if __name__ == "__main__":
    main()
