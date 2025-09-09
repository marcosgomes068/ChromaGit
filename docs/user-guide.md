# 📖 Guia do Usuário - ChromaGit

## Bem-vindo ao ChromaGit!

O ChromaGit é um sistema de controle de versão moderno que oferece uma experiência rica e intuitiva para gerenciar seus projetos.

## 🎯 Primeiros Passos

### 1. Iniciando um Repositório

```bash
# Modo interativo
python main.py
# Digite: init

# Ou diretamente
python main.py init
```

Isso criará a pasta `.chromagit/` com toda a estrutura necessária:
- `config.json` - Configurações do repositório
- `staging.json` - Área de staging para commits
- `commits.json` - Histórico de commits
- `backups/` - Backups automáticos

### 2. Adicionando Arquivos

```bash
# Adicionar todos os arquivos
python main.py add .

# Adicionar arquivos específicos
python main.py add arquivo.py outro.txt

# Adicionar por padrão
python main.py add *.py
```

### 3. Fazendo Commits

```bash
# Commit simples
python main.py commit -m "Minha primeira versão"

# Commit com estatísticas
python main.py commit -m "Nova funcionalidade" --stats

# Commit interativo (será solicitada mensagem)
python main.py commit
```

### 4. Visualizando o Histórico

```bash
# Ver todos os commits
python main.py log

# Limitar quantidade
python main.py log --limit 5

# Ver estatísticas detalhadas
python main.py log --stats
```

### 5. Sincronização Remota

```bash
# Push básico
python main.py push

# Push com nome específico do projeto
python main.py push -p "meu-projeto-v2"

# Push forçado (sobrescreve)
python main.py push --force
```

## 🎨 Modo Interativo

O modo interativo é a forma mais intuitiva de usar o ChromaGit:

```bash
python main.py
```

### Recursos do Modo Interativo:
- **Status em Tempo Real**: Veja o estado do repositório
- **Guia Rápido**: Comandos essenciais sempre visíveis
- **Tabela de Comandos**: Status de disponibilidade
- **Navegação Intuitiva**: Digite comandos naturalmente

### Comandos Especiais no Modo Interativo:
- `status` - Atualiza informações do repositório
- `clear` ou `cls` - Limpa a tela
- `exit`, `quit` ou `q` - Sai do modo interativo

## 🔧 Comandos Avançados

### Comando Init
```bash
# Inicialização básica
python main.py init

# Com nome específico
python main.py init --name "Meu Projeto"

# Forçar reinicialização
python main.py init --force
```

### Comando Add
```bash
# Adicionar recursivamente
python main.py add . --recursive

# Verificar antes de adicionar
python main.py add arquivo.py --verify

# Modo verbose
python main.py add . --verbose
```

### Comando Commit
```bash
# Commit com autor
python main.py commit -m "Nova feature" --author "João Silva"

# Commit com timestamp específico
python main.py commit -m "Correção" --timestamp "2025-01-01T10:00:00"

# Commit com estatísticas
python main.py commit -m "Update" --stats
```

### Comando Push
```bash
# Push para pasta específica
python main.py push -p "projeto-final"

# Push com backup
python main.py push --backup

# Push verbose
python main.py push --verbose
```

## 📊 Entendendo o Status

O comando `status` mostra informações importantes:

```
╭──────────── Status do Repositório ─────────────╮
│ ✓ Repositório ChromaGit ativo                  │
│ Arquivos em staging: 3                         │
│ Total de commits: 15                           │
│ Diretório: MeuProjeto                          │
│ Remoto: 🔄 Sincronizado                        │
╰────────────────────────────────────────────────╯
```

### Indicadores:
- **✓ Repositório ativo**: ChromaGit foi inicializado
- **Arquivos em staging**: Quantos arquivos prontos para commit
- **Total de commits**: Histórico de versões
- **Diretório**: Nome do projeto atual
- **Status remoto**: Estado da sincronização

## 🔄 Workflow Recomendado

1. **Inicializar**: `python main.py init`
2. **Adicionar**: `python main.py add .`
3. **Commit**: `python main.py commit -m "Descrição"`
4. **Repetir**: Adicionar → Commit conforme necessário
5. **Sincronizar**: `python main.py push` periodicamente

## 🆘 Solução de Problemas

### Repositório não inicializado
```
Erro: Este diretório não é um repositório ChromaGit
```
**Solução**: Execute `python main.py init`

### Nenhum arquivo em staging
```
Erro: Nenhum arquivo em staging para commit
```
**Solução**: Execute `python main.py add .` primeiro

### Erro de sincronização
```
Erro: Falha ao sincronizar com repositório remoto
```
**Solução**: Verifique o arquivo `.env` e configurações de rede

## 💡 Dicas e Truques

### 1. Uso do .gitignore
O ChromaGit respeita arquivos `.gitignore`. Adicione padrões para ignorar:
```
*.log
node_modules/
.env
__pycache__/
```

### 2. Mensagens de Commit Úteis
- Use presente do indicativo: "Adiciona nova funcionalidade"
- Seja específico: "Corrige bug no sistema de login"
- Use categorias: "[FIX]", "[FEAT]", "[DOCS]"

### 3. Organização com Push
Use nomes descritivos para pushes:
```bash
python main.py push -p "website-v1.0"
python main.py push -p "app-mobile-beta"
```

### 4. Backup Automático
O ChromaGit faz backup automático antes de:
- Commits importantes
- Operações de push
- Reinicializações

## 🔗 Próximos Passos

- Explore o [Guia do Desenvolvedor](developer-guide.md)
- Consulte a [Referência de Comandos](commands.md)
- Aprenda sobre o [Sistema de Push](push-system.md)
