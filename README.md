# qBittorrent Extensions

Este repositório contém extensões e plugins de busca personalizados para o qBittorrent. O objetivo é migrar e adaptar scripts de outras plataformas para funcionar nativamente na engine de busca do qBittorrent.

## 📁 Estrutura do Projeto

- **`src/`**: Diretório principal onde ficam as extensões criadas e prontas (ou em desenvolvimento) para o qBittorrent.
- **`source/`**: Arquivos e scripts de referência de outros projetos que servem como base para a migração para o qBittorrent.
- **`test/`**: Diretório destinado aos arquivos e scripts de testes das extensões.
- **`search-plugins/wiki/`**: Clone local da documentação oficial do qBittorrent Search Plugins Wiki, para consulta offline e referência rápida durante o desenvolvimento.

## 📥 Extensões Disponíveis

Você pode instalar as extensões individualmente colando os links abaixo no qBittorrent (na aba *Buscar* -> *Search plugins* -> *Install a new one* -> *Web link*), ou baixar todas de uma vez através do [último Release em ZIP](https://github.com/Jhoorodre/qbittorrent-ext/releases/latest).

* **Amigos Share Club**:
```text
https://raw.githubusercontent.com/Jhoorodre/qbittorrent-ext/main/src/amigosshareclub-qb/amigosshareclub.py
```

* **Dark Mahou**:
```text
https://raw.githubusercontent.com/Jhoorodre/qbittorrent-ext/main/src/darkmahou-qb/darkmahou.py
```

## 🛠️ Ferramenta de Automação (`manage.sh`)

Este repositório conta com um script bash próprio de automação para facilitar a vida do desenvolvedor, desde a criação de novos plugins até a checagem e envio de código. Comandos disponíveis:

* **Criar uma nova extensão do zero:**
  ```bash
  ./manage.sh new "Nome da Extensão"
  ```
  Ele cria a pasta em `src/`, gera o código Python boilerplate mínimo do qBittorrent, e injeta o bloco de texto com o botão de copiar aqui mesmo neste README, tudo de uma vez.

* **Validar código e fazer o Release (Push):**
  ```bash
  ./manage.sh push "Mensagem do seu commit"
  ```
  Ele obriga a checagem rigorosa de qualidade usando o linter **Ruff**. Se os testes passarem, o script empurra os códigos, incrementa uma nova **Tag** automática, e aciona o robô do GitHub para compilar o arquivo `.zip` na aba de Releases.

## 🚀 Roadmap de Desenvolvimento
Abaixo estão as extensões listadas por status de desenvolvimento:

### ✅ Concluídos
- [x] **amigosshareclub-qb**: Plugin de busca concluído.
- [x] **darkmahou-qb**: Plugin de busca concluído.

### 🚧 Em Desenvolvimento
*(Nenhuma no momento)*