# ChromaGit - Comandos e Lógica

## init
- Inicializa um repositório ChromaGit  
- Cria pasta oculta `.chromagit`  
- Cria arquivo de configuração inicial  
- Define branch principal `main`  
- Inicializa log de commits  
- Prepara estrutura interna para rastrear pacotes  
- Garante compatibilidade com o SO atual  

## add
- Adiciona arquivos ao staging do repositório  
- Valida existência do arquivo  
- Marca arquivo para próximo commit  
- Atualiza índice interno de rastreamento  
- Permite wildcards e pastas inteiras  
- Checa conflitos com arquivos já versionados  

## commit
- Salva alterações do staging no repositório  
- Registra data, hora e autor do commit  
- Gera hash único para cada commit  
- Permite mensagem curta ou detalhada  
- Atualiza histórico de commits  
- Atualiza estado dos pacotes instalados  

## install
- Instala dependências ou ferramentas externas  
- Detecta tipo de pacote: pip, executável, script  
- Baixa e instala automaticamente no projeto  
- Atualiza log interno de pacotes  
- Permite instalação global ou local ao projeto  
- Retorna status de sucesso ou falha  

## uninstall
- Remove pacote ou ferramenta instalada  
- Verifica dependências antes da remoção  
- Atualiza log interno e cache de pacotes  
- Permite remoção total ou parcial  
- Notifica usuário sobre conflitos  

## run
- Executa scripts dentro do repositório  
- Respeita pacotes instalados e configurações  
- Suporta Python, Node, Shell e binários  
- Captura saída do script para log  
- Permite parâmetros adicionais  
- Pode executar em background ou foreground  

## status
- Mostra estado atual do repositório  
- Lista arquivos modificados e staged  
- Lista pacotes instalados e suas versões  
- Exibe branch atual e último commit  
- Indica erros ou pacotes faltantes  
- Pode gerar relatório resumido ou completo  

## log
- Mostra histórico de commits  
- Permite filtros por autor, data ou mensagem  
- Exibe hash, mensagem e timestamp  
- Suporta visualização resumida ou detalhada  
- Pode exportar log para arquivo externo  

## exec
- Executa comando do sistema no contexto do projeto  
- Suporta Windows, Linux e macOS  
- Captura saída e erros  
- Atualiza log de execução  
- Permite execução interativa ou silenciosa  

## fetch
- Baixa arquivos da web e organiza no projeto  
- Suporta URLs HTTP/HTTPS  
- Salva no diretório especificado  
- Valida integridade do arquivo baixado  
- Atualiza log de recursos do projeto  
