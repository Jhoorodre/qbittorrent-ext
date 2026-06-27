qBittorrent fornece um sistema de gerenciamento de plug-ins de mecanismo de pesquisa.
Graças a isso, você pode *facilmente* escrever seus próprios plug-ins para procurar torrents em seus mecanismos de pesquisa Bittorrent favoritos e estender o mecanismo de pesquisa integrado qBittorrent.

* Tudo que você precisa é de alguma motivação e algum conhecimento da [linguagem Python](https://www.python.org).
* **A versão mínima suportada do python é especificada [aqui](https://github.com/qbittorrent/qBittorrent/blob/master/INSTALL#L21-L23), certifique-se de que seu plugin possa funcionar com ele e com todas as versões posteriores.**
* **Importe apenas bibliotecas da [Biblioteca padrão do Python](https://docs.python.org/3/library/index.html)**. \
Bibliotecas de terceiros (como aquelas instaladas a partir do [PyPI](https://pypi.org/)) ***não*** têm presença garantida no ambiente do usuário.
* Recomendamos que você garanta a boa qualidade do seu plugin: [Qualidade do código Python: ferramentas e práticas recomendadas](https://realpython.com/python-code-quality/). \
Por exemplo, aqui está como os plug-ins oficiais são verificados: [ci.yaml](https://github.com/qbittorrent/search-plugins/blob/60a3f4d9c97a5d1f94e75789a72ee054044c5802/.github/workflows/ci.yaml#L29-L44).


#ÍNDICE
## [Especificação de plug-ins](How-to-write-a-search-plugin.md#plugins-specification-1)

### 1.1 [Formato dos resultados da pesquisa](How-to-write-a-search-plugin.md/#search-results-format)

### 1.2 [Estrutura de arquivo de classe Python](How-to-write-a-search-plugin.md/#python-class-file-structure)

### 1.3 [Análise de resultados de páginas da Web](How-to-write-a-search-plugin.md/#parsing-results-from-web-pages)

## [Compreendendo o código](How-to-write-a-search-plugin.md#understanding-the-code-1)

### 2.1 [Função auxiliar do PrettyPrinter](How-to-write-a-search-plugin.md#prettyprinter-helper-function)

### 2.2 [Função auxiliar Retrieve_URL](How-to-write-a-search-plugin.md#retrieve_url-helper-function)

### 2.3 [Função auxiliar Download_File](How-to-write-a-search-plugin.md#download_file-helper-function)

## [Testando e finalizando seu código](How-to-write-a-search-plugin.md#testing--finalizing-your-code-1)

### 3.1 [Exemplos de código](How-to-write-a-search-plugin.md/#code-examples)

### 3.2 [Testando seu plug-in](How-to-write-a-search-plugin.md#testing-your-plugin)

### 3.3 [Instale seu plug-in](How-to-write-a-search-plugin.md#install-your-plugin)

### 3.4 [Publique seu plug-in](How-to-write-a-search-plugin.md#publish-your-plugin)

### 3.5 [Notas](How-to-write-a-search-plugin.md#notes)


# Especificação de plug-ins

*⚠️O plugin comunica dados de volta ao qBittorrent via stdout e isso significa que você NÃO deve imprimir mensagens de depuração/erro no stdout sob nenhuma circunstância. Você pode imprimir as mensagens de depuração/erro em stderr.*

## Formato dos resultados da pesquisa
Primeiro, você deve entender que um plugin de mecanismo de busca qBittorrent é na verdade um arquivo de classe Python cuja tarefa é entrar em contato com o site de um mecanismo de busca (por exemplo, [The Pirate Bay](https://www.thepiratebay.org)), analisar os resultados exibidos pela página da web e imprimi-los em stdout com a seguinte sintaxe:
```
link|name|size|seeds|leech|engine_url|desc_link|pub_date
```

Um resultado de pesquisa por linha.

Por exemplo:
```
magnet:?xt=urn:btih:5F5E8848426129AB63CB4DB717BB54193C1C1AD7&dn=ubuntu-20.04.6-desktop-amd64.iso|ubuntu-20.04.6-desktop-amd64.iso|4351463424|15|2|https://thepiratebay.org|https://thepiratebay.org/description.php?id=72774917|1696870394
magnet:?xt=urn:btih:07053761979D09DEAD94D09E8326DB919797B078&dn=ubuntu-10.04-server-i386.iso|ubuntu-10.04-server-i386.iso|700413952|1|0|https://thepiratebay.org|https://thepiratebay.org/description.php?id=5551290|1273547377
```

## Estrutura do arquivo de classe Python
Seu plugin deve se chamar "engine_name.py", em letras minúsculas e sem espaços nem caracteres especiais.
Você também precisará dos outros arquivos do projeto ([Link](https://github.com/qbittorrent/qBittorrent/tree/master/src/searchengine/nova3))

Os arquivos são:

```
-> nova2.py # the main search engine script which calls the plugins
-> nova2dl.py # standalone script called by qBittorrent to download a torrent using a particular search plugin
-> helpers.py # contains helper functions you can use in your plugins such as retrieve_url() and download_file()
-> novaprinter.py # contains some useful functions like prettyPrint(my_dict) to display your search results
-> socks.py # Required by helpers.py. This module provides a standard socket-like interface.
```


Aqui está a estrutura básica de engine_name.py:
```python
#VERSION: 1.00
# AUTHORS: YOUR_NAME (YOUR_MAIL)
# LICENSING INFORMATION

from html.parser import HTMLParser
from helpers import download_file, retrieve_url
from novaprinter import prettyPrinter
# some other imports if necessary

class engine_name(object):
    """
    `url`, `name`, `supported_categories` should be static variables of the engine_name class,
     otherwise qbt won't install the plugin.

    `url`: The URL of the search engine.
    `name`: The name of the search engine, spaces and special characters are allowed here.
    `supported_categories`: What categories are supported by the search engine and their corresponding id,
    possible categories are ('all', 'anime', 'books', 'games', 'movies', 'music', 'pictures', 'software', 'tv').
    """

    url = 'https://www.engine-url.org'
    name = 'Full engine name'
    supported_categories = {
        'all': '0',
        'anime': '7',
        'games': '2',
        'movies': '6',
        'music': '1',
        'software': '3',
        'tv': '4'
    }

    def __init__(self):
        """
        Some initialization
        """

    def download_torrent(self, info):
        """
        Providing this function is optional.
        It can however be interesting to provide your own torrent download
        implementation in case the search engine in question does not allow
        traditional downloads (for example, cookie-based download).
        """
        print(download_file(info))

    # DO NOT CHANGE the name and parameters of this function
    # This function will be the one called by nova2.py
    def search(self, what, cat='all'):
        """
        Here you can do what you want to get the result from the search engine website.
        Everytime you parse a result line, store it in a dictionary
        and call the prettyPrint(your_dict) function.

        `what` is a string with the search tokens, already escaped (e.g. "Ubuntu+Linux")
        `cat` is the name of a search category in ('all', 'anime', 'books', 'games', 'movies', 'music', 'pictures', 'software', 'tv')
        """
```

**OBSERVE que o nome do arquivo (sem extensão .py) deve ser idêntico ao nome da classe. Caso contrário, o qBittorrent se recusará a instalá-lo!**

## Analisando resultados de páginas da web
Depois de baixar o conteúdo da página web que contém os resultados (usando `retrieve_url()`), você vai querer analisá-lo para criar um `dict` por resultado de pesquisa e chamar a função `prettyPrint(your_dict)` para exibi-lo no stdout (em um formato compreensível pelo qBittorrent).

Para analisar as páginas, você pode usar os seguintes módulos python (não exaustivos):
* **[MÉTODO ACONSELHADO]** [HTMLParser](https://docs.python.org/2/library/htmlparser.html) / [html.parser](https://docs.python.org/3/library/html.parser.html): analisador python integrado que substitui o SGMLParser obsoleto. Principalmente semelhante ao SMGLParser
* `xml.dom.minidom`: analisador XML. Tenha cuidado, este analisador é muito sensível e o site deve ser totalmente compatível com XHTML para que funcione.
* `re`: Se você gosta de usar expressões regulares (regex)

Observe que o tamanho está em bytes fornecidos.

Para realizar esta tarefa, fornecemos várias funções auxiliares, como `prettyPrinter()`.

# Compreendendo o código
## Função auxiliar `prettyPrinter()`
Na verdade, você realmente não precisa prestar atenção à sintaxe de saída porque fornecemos uma função para isso chamada `prettyPrinter(dictionary)`. Você pode importá-lo usando o seguinte comando:
```python
from novaprinter import prettyPrinter
```

Você deve passar para esta função um dicionário contendo as seguintes chaves (o valor deve ser `-1` se você não tiver a informação):
* `link` => Uma string correspondente ao link de download (o arquivo .torrent ou link magnético)
* `name` => Uma string unicode correspondente ao nome do torrent (ou seja: "Ubuntu Linux v6.06")
* `size` => Uma string correspondente ao tamanho do torrent (ou seja: "6 MB" ou "200 KB" ou "1,2 GB"...)
* `seeds` => O número de sementes para este torrent (como uma string)
* `leech` => O número de leechers para este torrent (a a string)
* `engine_url` => O URL do mecanismo de pesquisa (ou seja: https://www.mininova.org)
* `desc_link` => Uma string correspondente à página de descrição do torrent
* `pub_date` => Um carimbo de data/hora unix correspondente à data de publicação do torrent (ou seja: 1696870394)

## função auxiliar `retrieve_url()`
O método `retrieve_url()` recebe uma URL como parâmetro e retorna o conteúdo da URL como uma string.<br />
Esta função é útil para obter os resultados da pesquisa de um site de mecanismo de pesquisa Bittorrent. Tudo que você precisa fazer é passar o URL formatado corretamente para a função (o URL geralmente inclui parâmetros GET relativos a tokens de pesquisa, categoria, classificação, número de página).

```python
from helpers import retrieve_url
dat = retrieve_url(self.url + '/search?q=%s&c=%s&o=52&p=%d' % (what, self.supported_categories[cat], i))
```

## função auxiliar `download_file()`
As funções `download_file()` tomam como parâmetro a URL de um arquivo torrent. Esta função irá baixar o torrent para um local temporário e imprimir em stdout:
```shell
path_to_temporary_file url
```

Ele imprime dois valores separados por um espaço:
* O caminho para o arquivo baixado (geralmente na pasta /tmp)
* A URL da qual o arquivo foi baixado

Aqui está um exemplo:
```python
from helpers import retrieve_url, download_file
print download_file(url)
> /tmp/esdzes https://www.mininova.org/get/123456
```
# Testando e finalizando seu código

## Exemplos de código
Não hesite em usar os plug-ins oficiais do mecanismo de pesquisa como exemplo. Eles estão disponíveis [aqui](https://github.com/qbittorrent/search-plugins/tree/master/nova3/engines).
* kickasstorrents.py usa módulo json
* torrentreactor.py usa o módulo HTMLParser

## Testando seu plug-in
Antes de instalar seu plugin (no Qbittorrent), você pode testar a execução do plugin enquanto o depura. Portanto, recomendamos que você baixe [estes arquivos](https://github.com/qbittorrent/qBittorrent/tree/master/src/searchengine/nova3).

Você obterá a seguinte estrutura:
```
your_search_engine
-> nova2.py # the main search engine script which calls the plugins
-> nova2dl.py # standalone script called by qBittorrent to download a torrent using a particular search plugin
-> helpers.py # contains helper functions you can use in your plugins such as retrieve_url() and download_file()
-> novaprinter.py # contains some useful functions like prettyPrint(my_dict) to display your search results
-> socks.py # Required by helpers.py. This module provides a standard socket-like interface.
```

Coloque seu plugin na pasta `engines/` ( %localappdata%\qBittorrent\nova3\engines\ ) e então no CMD execute o script nova2.py assim:
```shell
..\nova2.py your_search_engine_name category search_tokens
# e.g.: ..\nova2.py mininova all kubuntu linux
# e.g.: ..\nova2.py btjunkie books ubuntu
```

Um resultado bem-sucedido produzirá:
```
DEBUG:root:C:\users\user\appdata\local\qbittorrent\nova3\qbt\qbt
the app will start listing links it finds in the following format:
link|name|size|#seeds|#leechers|engine|page url
```

## Instale seu plug-in
1. Vá para a aba de pesquisa na janela principal, clique no botão "Mecanismos de pesquisa...".
2. Em seguida, uma nova janela aparecerá, contendo a lista de plug-ins de mecanismos de busca instalados.
3. Clique em "Instalar um novo" na parte inferior e selecione seu script python `*.py` em seu sistema de arquivos.<br />
Se tudo correr bem, o qBittorrent deverá notificá-lo de que foi instalado com sucesso e seu plugin deverá aparecer na lista.

## Publique seu plug-in
Depois que você conseguir escrever um plug-in de mecanismo de pesquisa para qBittorrent que funcione, sinta-se à vontade para publicá-lo nesta página wiki (https://plugins.qbittorrent.org) para que outros usuários possam usá-lo também.<br />
Se você tiver sorte, seu plugin também poderá estar incluído no [repositório oficial](https://github.com/qbittorrent/search-plugins).

## Notas
* Como convenção, é aconselhável imprimir os resultados classificados por número de sementes (o maior número de sementes no topo) porque geralmente são os torrents mais interessantes.
* Observe que os mecanismos de pesquisa geralmente exibem resultados em várias páginas. Portanto, é melhor analisar todas essas páginas para obter todos os resultados. Todos os plugins oficiais têm suporte para várias páginas.
* Alguns motores de busca não fornecem todas as informações exigidas por `prettyPrinter()`. Se for o caso, defina `-1` como valor para a chave fornecida (ou seja: `torrent_info['seeds'] = -1`)
* Plugins empacotados em python não podem mais ser instalados diretamente desde qBittorrent v2.0.0. Você deve fornecer ao qBittorrent o arquivo python.
