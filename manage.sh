#!/bin/bash
# ponytail: bash automation replacing complex CI pipelines with 2 commands
# Usage: ./manage.sh new "Plugin Name" | ./manage.sh push "Commit message"

if [ "$1" = "new" ]; then
    # ponytail: one-liner slug generation
    slug=$(echo "$2" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-' | sed 's/-$//')
    mkdir -p "src/$slug"
    
    # ponytail: minimal template injection
    cat <<EOF > "src/$slug/$slug.py"
# VERSION: 1.00
import re
import urllib.parse
import urllib.request
from novaprinter import prettyPrinter

class $slug:
    # ponytail: minimal qbittorrent plugin structure
    url, name, supported_categories = 'https://example.com', '$2', {'all': ''}

    def search(self, what, cat='all'):
        pass # ponytail: implement your search here
EOF
    
    # ponytail: automatic README injection with copyable code block
    raw="https://raw.githubusercontent.com/Jhoorodre/qbittorrent-ext/main/src/$slug/$slug.py"
    sed -i "/^## 🛠️ Ferramenta/i * **$2**:\n\`\`\`text\n$raw\n\`\`\`\n" README.md
    sed -i "/^### 🚧 Em Desenvolvimento/a - [ ] **$slug**: Plugin em desenvolvimento." README.md
    echo "[✓] Extensão '$2' criada em src/$slug/ e adicionada ao README e ao Roadmap!"

elif [ "$1" = "push" ]; then
    # ponytail: local lint + push normal
    ruff check src/ --fix || { echo "[X] Falha no Ruff! Corrija os erros antes de fazer o push."; exit 1; }
    
    git add .
    git commit -m "${2:-"Atualização de desenvolvimento"}"
    git push origin main
    
    echo "[✓] Commit feito e enviado para a branch main!"

else
    echo "Uso: ./manage.sh new \"Nome da Extensao\"  |  ./manage.sh push \"Mensagem do Commit\""
fi
