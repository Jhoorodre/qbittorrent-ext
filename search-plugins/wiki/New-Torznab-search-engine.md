Este guia irá ajudá-lo a configurar o novo mecanismo de busca qBittorrent.

## Aviso de descontinuação

Até a versão 4.5.0, o qBittorrent tinha um mecanismo de busca nativo baseado em Python. A equipe qBittorrent ficou encarregada de verificar a instalação do Python e a manutenção dos [plugins de busca](https://github.com/qbittorrent/search-plugins) para os sites de torrent. Havia também [plugins não oficiais](Unofficial-search-plugins.media.md) mantidos pela comunidade.

Com o passar do tempo, a manutenção deste sistema tornou-se um fardo devido ao grande número de sites de torrent e à falta de desenvolvedores com conhecimento de Python.
Desde a versão 4.5.0, o mecanismo de busca nativo foi substituído por um novo mecanismo de busca que faz chamadas para [APIs compatíveis com Torznab](https://torznab.github.io/spec-1.3-draft/torznab/Specification-v1.3.html). Isto implica que o usuário final deve instalar software adicional para realizar pesquisas no qBittorrent.

## Clientes Torznab

[Torznab](https://torznab.github.io/spec-1.3-draft/torznab/Specification-v1.3.html) é uma especificação de API baseada na Newznab WebAPI. A API é construída em torno de um feed XML/RSS simples com recursos de filtragem e paginação.

Existem vários softwares compatíveis com esta especificação. Seu objetivo é oferecer suporte ao maior número possível de sites de torrent, analisar o conteúdo e converter os resultados para o formato Torznab para que possam ser consumidos por outros aplicativos como o qBittorrent.

Estes são os aplicativos mais populares:
* [Jackett](https://github.com/Jackett/Jackett): **(recomendado)**. Suporta mais de 500 sites de torrent e possui a maior base de usuários.
* [Prowlarr](https://github.com/Prowlarr/Prowlarr): Suporta os mesmos sites que Jackett, mas com uma interface de usuário mais moderna.
* [NZB Hydra](https://github.com/theotherp/nzbhydra2): Inclui mais recursos, mas oferece suporte a menos sites de torrent.
* [Cardigann](https://github.com/cardigann/cardigann): Alguns sites ainda funcionam, mas não são mais mantidos.

Todos eles funcionam bem no qBittorrent, mas fornecemos apenas instruções para Jackett.

## Instalação da jaqueta
[Jackett](https://github.com/Jackett/Jackett) está disponível para Windows, Linux e macOS. Também está disponível como contêiner Docker e pacote de distribuição Linux.

Você pode encontrar as instruções de instalação [aqui](https://github.com/Jackett/Jackett#installation-on-windows). É realmente recomendado instalar o Jackett como um serviço do sistema. Desta forma, iniciará automaticamente ao iniciar o computador e estará sempre atualizado.

Assim que o Jackett estiver instalado. Você pode abrir a UI da Web para configurar os sites de torrent. O URL do Jackett geralmente é http://127.0.0.1:9117. A próxima etapa é configurar seus sites de torrent favoritos. Clique no botão "Adicionar indexador" e siga as instruções.

![](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/wiki/qbittorrent_torznab_search_1.png)

Quando terminar, use a “Pesquisa manual” para verificar se funciona corretamente.

![](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/wiki/qbittorrent_torznab_search_2.png)

## mecanismo de pesquisa qBittorrent

Por padrão, o mecanismo de pesquisa está desativado. Você pode habilitá-lo em "Visualizar => Mecanismo de pesquisa".

![](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/wiki/qbittorrent_torznab_search_3.png)

Agora você verá uma nova aba onde poderá pesquisar e configurar os “Indexadores” (sites de torrent).

![](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/wiki/qbittorrent_torznab_search_4.png)

Você deve adicionar os indexadores um por um. O nome pode ser qualquer coisa. O URL do Toznab e a chave de API são copiados da UI da Web do Jackett.

![](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/wiki/qbittorrent_torznab_search_5.png)

![](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/wiki/qbittorrent_torznab_search_6.png)

Os indexadores podem ser desabilitados e editados com o "menu do botão direito".

![](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/wiki/qbittorrent_torznab_search_7.png)

Você pode realizar pesquisas em todos os indexadores habilitados normalmente.

![](https://raw.githubusercontent.com/qbittorrent/search-plugins/master/wiki/qbittorrent_torznab_search_8.png)

Se algum indexador não estiver funcionando conforme o esperado (ou você não obtiver nenhum resultado), verifique os logs qBittorrent e Jackett para obter mais detalhes.
