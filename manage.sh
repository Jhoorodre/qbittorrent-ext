#!/bin/bash
# ponytail: bash automation replacing complex CI pipelines with 2 commands
# Usage: ./manage.sh new "Plugin Name" | ./manage.sh push "Commit message"

if [ "$1" = "new" ]; then
    # ponytail: one-liner slug generation
    slug=$(echo "$2" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9' '-' | sed 's/-$//' | sed 's/-qb$//')
    folder="${slug}-qb"
    mkdir -p "src/$folder"
    
    # ponytail: minimal template injection
    cat <<EOF > "src/$folder/$slug.py"
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
    raw="https://raw.githubusercontent.com/Jhoorodre/qbittorrent-ext/main/src/$folder/$slug.py"
    sed -i "/^## 🛠️ Ferramenta/i * **$2**:\n\`\`\`text\n$raw\n\`\`\`\n" README.md
    
    # Adiciona no roadmap de desenvolvimento salvando o nome bonito e a pasta
    sed -i "/^### 🚧 Em Desenvolvimento/a - [ ] **$2** (\`$folder\`): Plugin em desenvolvimento." README.md
    
    echo "[✓] Extensão '$2' criada em src/$folder/ e adicionada ao Roadmap!"

elif [ "$1" = "push" ]; then
    # ponytail: local lint + auto-bump tag + push
    ruff check src/ --fix || { echo "[X] Falha no Ruff! Corrija os erros antes de fazer o push."; exit 1; }
    
    # Move qualquer plugin 'em desenvolvimento' para 'concluídos' e adiciona o link
    sed -n '/^### 🚧 Em Desenvolvimento/,/^###/p' README.md | grep '^- \[ \]' | while read -r line; do
        # Extrai o nome bonito e a pasta a partir do novo formato do Roadmap
        pretty=$(echo "$line" | sed 's/^- \[ \] \*\*\(.*\)\*\* (`.*`):.*$/\1/')
        folder=$(echo "$line" | sed 's/^- \[ \] \*\*.*\*\* (`\(.*\)`):.*$/\1/')
        
        # Remove do desenvolvimento e adiciona nos concluídos usando o padrão do folder
        sed -i "/- \[ \] \*\*$pretty\*\* (\`$folder\`)/d" README.md
        sed -i "/^### ✅ Concluídos/a - [x] **$folder**: Plugin de busca concluído." README.md
        
        # Gera e injeta o bloco de texto para download nas Extensões Disponíveis com o nome original
        slug=${folder%-qb}
        raw="https://raw.githubusercontent.com/Jhoorodre/qbittorrent-ext/main/src/$folder/$slug.py"
        sed -i "/^## 🛠️ Ferramenta/i * **$pretty**:\n\`\`\`text\n$raw\n\`\`\`\n" README.md
    done
    
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
