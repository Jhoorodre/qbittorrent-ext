# Integração Jackett para qBittorrent

**qBittorrent** vem com alguns plug-ins de pesquisa. Embora estes sejam frequentemente
suficiente para a maioria dos usuários, aqueles que desejam realizar pesquisas em uma variedade mais ampla
dos sites de indexação têm a opção de instalar **[Jackett][jackett]** e
executá-lo em conjunto com o qBittorrent para aproveitar suas vantagens muito maiores
catálogo de indexadores (584, em novembro de 2025) e eficiência na recuperação de resultados
deles. Configure o **plugin Jackett qBittorrent** (essencialmente, defina a chave API).

## O que é jaqueta?

Conforme explicado no [arquivo README.md][jackett-readme] do projeto (ênfase adicionada):

> Jackett funciona como um servidor proxy: traduz consultas de aplicativos ([incluindo]
> qBittorrent […]) em consultas HTTP específicas do site para qualquer número de
> rastreadores [BitTorrent], analisa as respostas HTML ou JSON e, em seguida, envia o
> resultados de volta ao software solicitante. Isso permite obter informações recentes
> uploads (como RSS) e realização de pesquisas. Jackett é um repositório único de
> **mantida a lógica de extração e tradução do indexador** — eliminando a carga
> de outros aplicativos.

Mais claramente, embora o qBittorrent seja um gerenciador de downloads que evoluiu para
inclui alguns recursos integrados para descoberta de torrents, o Jackett foi desenvolvido especificamente para
software projetado para realizar essas mesmas pesquisas em uma escala muito maior. Um
um aplicativo como o qBittorrent pode apresentar as pesquisas que é solicitado a realizar
para Jackett, que os transmite para uma lista definida pelo usuário de potencialmente centenas
de indexação de sites de uma só vez e, em seguida, envia os resultados à medida que chegam.
As principais vantagens deste arranjo são três:

- Como realizar buscas é sua única função, é muito mais rápido na realização
e processando os resultados.
- A capacidade de realizar pesquisas em índices de lista muito mais amplos e rápidos de
adicione novos sites e remova os mortos.
- É muito melhor reagir às mudanças frequentes que ocorrem no
sites indexadores que surgem enquanto trabalham para mitigar tentativas de interromper seu
operação.

As atualizações em seu catálogo de indexadores ocorrem quase diariamente e incluem
centenas de sites que nunca tiveram nem provavelmente teriam seus próprios
Plug-in de pesquisa qBittorrent.

## Instalação

### Pré-requisitos

Jackett é construído usando o framework .NET e requer que você tenha o .NET 8
Tempo de execução presente em seu sistema antes da instalação. A Microsoft fornece
arquivos de instalação para o tempo de execução para [Windows][dotnet-windows-support],
[macOS][dotnet-macos-support] e [GNU/Linux][dotnet-linux-support] (clique no
links anteriores para ver os requisitos mínimos para cada sistema operacional).

**[Downloads do Microsoft .NET][downloads dotnet]**

**Guias oficiais de instalação do .NET**:

- [Windows][dotnet-windows-install]
- [macOS][dotnet-macos-install]
- [Linux][dotnet-linux-install]

### Jaqueta

Depois que o tempo de execução .NET estiver instalado, siga a documentação oficial vinculada
abaixo para instalar e configurar o Jackett.

- [Instalação no Windows][install-windows]
- Instalação em Linux:
- [AMD64 (x86_64)][instalar-linux-amd64]
- [ARMv7 e mais recente][install-linux-armv7]
- [ARMv6 e anteriores][install-linux-armv6]

### plugin qBitTorrent

> [!NOTA]
> O URL completo para download do arquivo do plugin é
> `https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/jackett.py`

Siga estas etapas para instalar manualmente o plugin:

1. Inicie o qBittorrent e clique na guia Pesquisar (mostrada apenas quando "Pesquisar
Engine" está ativo no menu Exibir)
1. Destaque o URL mostrado acima ou clique com o botão direito [neste link][arquivo de plugin] e
**copie** para a área de transferência
1. Clique no botão **Pesquisar plug-ins…** no canto inferior direito e clique em
**Instale um novo** e, finalmente, **Link da Web** como "Pesquisar fonte do plugin"
1. qBittorrent tenta preencher automaticamente o campo de entrada se um URL for encontrado em
a área de transferência, mas se não, cole manualmente o URL lá

## Configuração

> [!IMPORTANTE]
> Lembre-se de [iniciar o Jackett](https://github.com/Jackett/Jackett#supported-systems)
> primeiro. :)

O plugin Jackett usa um arquivo de configuração externo, garantindo que qualquer
atualizações no arquivo do plug-in não apagarão ou redefinirão suas configurações. O nome de
o arquivo de configuração é `jackett.json` e deve residir na mesma pasta
como os arquivos do plug-in de pesquisa qBittorrent, cujos padrões são:

- **Janelas:**
- Sintaxe CMD: `%LOCALAPPDATA%\qBittorrent\nova3\engines`
- Sintaxe do PowerShell: `"${Env:LOCALAPPDATA}\qBittorrent\nova3\engines"`
- **Linux:**
- `"${XDG_DATA_HOME:-$HOME/.local/share}/qBittorrent/nova3/engines"` (atual);
- `"${XDG_DATA_HOME:-$HOME/.local/share}/data/qBittorrent/nova3/engines"` (formulários)
- `"${HOME}/.var/app/org.qbittorrent.qBittorrent/data/qBittorrent/nova3/engines"`
- **macOS:** `"~/Library/Application Support/qBittorrent/nova3/engines"`

Se por algum motivo o arquivo de configuração não existir, crie um com o
seguintes conteúdos:

```json
{
    "api_key": "YOUR_API_KEY_HERE",
    "url": "http://127.0.0.1:9117",
    "tracker_first": false,
    "thread_count": 20
}
```

> [!TIP]
> Se estiver executando o qBittorrent no modo headless e acessando sua interface web
> remotamente, configuração padrão do Jackett para vincular ao endereço de loopback
> (127.0.0.1) deve ser substituído por um endereço roteável (por exemplo, usando DDNS
> ou um endereço Unicast global IPv6) para permitir que o tráfego passe entre ele e
> qBitTorrent. Regras adicionais de firewall ou encaminhamento de porta também podem ser necessárias.
>
> A alteração deve ser feita tanto na UI do Jackett quanto na configuração do plugin
> arquivo, especificamente sua chave `url`. Por exemplo:

```diff
 {
     "api_key": "YOUR_API_KEY_HERE",
-    "url": "http://127.0.0.1:9117",
+    "url": "http://yourserver.ddnsprovider.host:9117",
     "tracker_first": false,
     "thread_count": 20
 }
```

### Propriedades do arquivo de configuração

|  Property name  |      Initial value      |                                             Description                                             |
|:----------------|:------------------------|:----------------------------------------------------------------------------------------------------|
|    `api_key`    |   `YOUR_API_KEY_HERE`   | Jackett API Key, shown in the upper-right corner of the Jackett UI ([screenshot below][api-key-ss]) |
|      `url`      | `http://127.0.0.1:9117` | Jackett service address (without a terminating forward slash)                                       |
| `tracker_first` |         `false`         | Prepend indexer site name to each search result (takes Boolean value)                               |
| `thread_count`  |          `20`           | Maximum number of concurrent requests to Jackett (to disable concurrent requests, set value to `1`) |

## Desativando/Removendo o plugin Jackett

O plugin Jackett está habilitado por padrão no qBittorrent. No entanto, você pode
desative-o ou remova-o totalmente a qualquer momento seguindo estas etapas:

1. Na guia **Pesquisar**, clique no botão **Pesquisar plug-ins…** na
canto inferior direito.
1. Localize a entrada chamada **Jackett** na lista.
1. Para desabilitar o plugin:
- Clique com o botão direito na entrada e desmarque a opção **Ativado**.

Ou para desinstalar o plugin:
- Clique com o botão direito na entrada e selecione **Desinstalar**.
1. Clique no botão **Fechar**.

## Capturas de tela

### Chave API Jackett

![Jackett UI screenshot showing API Key location][api-key]

### Resultados da pesquisa

Depois de instalar com sucesso o Jackett e integrá-lo ao qBittorrent, o
os resultados que ele fornece aparecem conforme mostrado abaixo.

![qBittorrent search tab with Jackett results][search-tab-results]

[jackett]: https://github.com/Jackett/Jackett "Jackett: suporte API para seus rastreadores de torrent favoritos"
[jacket-readme]: https://github.com/Jackett/Jackett/blob/master/README.md "Jacket: README.md"
[dotnet-windows-support]: https://github.com/dotnet/core/blob/main/release-notes/8.0/supported-os.md#windows
[dotnet-macos-support]: https://github.com/dotnet/core/blob/main/release-notes/8.0/supported-os.md#macos
[dotnet-linux-support]: https://github.com/dotnet/core/blob/main/release-notes/8.0/supported-os.md#linux
[dotnet-downloads]: https://dotnet.microsoft.com/download/dotnet/8.0
[dotnet-windows-install]: https://github.com/dotnet/core/blob/main/release-notes/8.0/install-windows.md
[dotnet-macos-install]: https://github.com/dotnet/core/blob/main/release-notes/8.0/install-macos.md
[dotnet-linux-install]: https://github.com/dotnet/core/blob/main/release-notes/8.0/install-linux.md
[instalar janelas]: https://github.com/Jackett/Jackett#installation-on-windows
[instalar-linux-amd64]: https://github.com/Jackett/Jackett#installation-on-linux-amdx64
[instalar-linux-armv7]: https://github.com/Jackett/Jackett#installation-on-linux-armv7-or-above
[instalar-linux-armv6]: https://github.com/Jackett/Jackett#installation-on-linux-armv6-or-below
[arquivo de plug-in]: https://raw.githubusercontent.com/qbittorrent/search-plugins/master/nova3/engines/jackett.py
[api-key-ss]: #jackett-api-key
[chave de API]: https://i.imgur.com/87yZeAU.png
[resultados da guia de pesquisa]: https://i.imgur.com/uCawgLa.png
