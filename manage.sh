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
import urllib.request, urllib.parse, re
from novaprinter import prettyPrinter

class $slug:
    # ponytail: minimal qbittorrent plugin structure
    url, name, supported_categories = 'https://example.com', '$2', {'all': ''}

    def search(self, what, cat='all'):
        pass # ponytail: implement your search here
EOF
    
    # ponytail: automatic README injection with copyable code block
    raw="https://raw.githubusercontent.com/Jhoorodre/qbittorrent-ext/main/src/$slug/$slug.py"
    sed -i "/^## 🚀 Roadmap/i * **$2**:\n\`\`\`text\n$raw\n\`\`\`\n" README.md
    echo "[✓] Extensão '$2' criada em src/$slug/ e link adicionado ao README!"

elif [ "$1" = "push" ]; then
    # ponytail: local lint + auto-bump tag + push
    ruff check src/ --fix || { echo "[X] Falha no Ruff! Corrija os erros antes de fazer o push."; exit 1; }
    
    git add .
    git commit -m "${2:-"Atualização automática dos plugins"}"
    
    # auto increment patch version (ex: v1.0.3 -> v1.0.4)
    tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "v1.0.0")
    if git rev-parse "$tag" >/dev/null 2>&1; then
        tag=$(echo "$tag" | awk -F. -v OFS=. '{$NF += 1 ; print}')
    fi
    
    git tag "$tag"
    git push origin main
    git push origin "$tag"
    echo "[✓] Commit feito, tag $tag gerada e enviada! O GitHub Actions vai gerar o .zip agora."

else
    echo "Uso: ./manage.sh new \"Nome da Extensao\"  |  ./manage.sh push \"Mensagem do Commit\""
fi
