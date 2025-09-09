#!/usr/bin/env python3
"""
Build simples do ChromaGit com favicon
"""

import subprocess
import sys
from pathlib import Path

def build_with_icon():
    """Compila o main.py com ícone do favicon"""
    print("🔨 Compilando ChromaGit com ícone...")
    
    # Verificar se favicon existe
    favicon_path = Path("favicon.ico").resolve()
    
    if favicon_path.exists():
        print(f"✅ Favicon encontrado: {favicon_path}")
        icon_param = ["--icon", str(favicon_path)]
    else:
        print("⚠️ Favicon não encontrado, usando ícone padrão")
        icon_param = []
    
    # Comando de compilação
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",
        "--name", "ChromaGit",
        "main.py",
        "--distpath", "obj",
        "--workpath", "obj/build",
        "--specpath", "obj",
        "--clean"
    ] + icon_param
    
    print(f"Executando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Build concluído com sucesso!")
        print("📁 Executável disponível em: obj/ChromaGit.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build: {e}")
        return False

def build_desktop_app():
    """Compila a aplicação desktop"""
    print("🖥️ Compilando aplicação desktop...")
    
    favicon_path = Path("favicon.ico").resolve()
    
    if favicon_path.exists():
        icon_param = ["--icon", str(favicon_path)]
    else:
        icon_param = []
    
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",
        "--windowed",  # Remove console window
        "--name", "ChromaGit-Desktop",
        "chromagit_desktop.py",
        "--distpath", "obj",
        "--workpath", "obj/build_desktop",
        "--specpath", "obj",
        "--clean"
    ] + icon_param
    
    print(f"Executando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Aplicação desktop compilada com sucesso!")
        print("📁 Aplicação disponível em: obj/ChromaGit-Desktop.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build da aplicação desktop: {e}")
        return False

def build_without_icon():
    """Compila sem ícone se o favicon não funcionar"""
    print("🔨 Compilando ChromaGit sem ícone...")
    
    cmd = [
        "python", "-m", "PyInstaller",
        "--onefile",
        "--name", "ChromaGit",
        "main.py",
        "--distpath", "obj",
        "--workpath", "obj/build",
        "--specpath", "obj",
        "--clean"
    ]
    
    print(f"Executando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Build sem ícone concluído com sucesso!")
        print("📁 Executável disponível em: obj/ChromaGit.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no build sem ícone: {e}")
        return False

if __name__ == "__main__":
    print("🌈 ChromaGit Build System")
    print("=" * 40)
    
    # Tentar build com ícone primeiro
    success_cli = build_with_icon()
    
    # Se falhar, tentar sem ícone
    if not success_cli:
        print("\n⚠️ Build com ícone falhou, tentando sem ícone...")
        success_cli = build_without_icon()
    
    # Build da aplicação desktop
    success_desktop = build_desktop_app()
    
    # Se falhar, tentar sem ícone
    if not success_desktop:
        print("\n⚠️ Build desktop com ícone falhou, tentando sem ícone...")
        cmd = [
            "python", "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name", "ChromaGit-Desktop",
            "chromagit_desktop.py",
            "--distpath", "obj",
            "--workpath", "obj/build_desktop",
            "--specpath", "obj",
            "--clean"
        ]
        try:
            result = subprocess.run(cmd, check=True)
            success_desktop = True
            print("✅ Aplicação desktop sem ícone compilada com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro no build desktop sem ícone: {e}")
    
    print("\n" + "=" * 40)
    if success_cli and success_desktop:
        print("🎉 Todos os builds concluídos com sucesso!")
    elif success_cli:
        print("✅ Build CLI concluído, ❌ Build desktop falhou")
    elif success_desktop:
        print("❌ Build CLI falhou, ✅ Build desktop concluído")
    else:
        print("❌ Todos os builds falharam")
        sys.exit(1)
