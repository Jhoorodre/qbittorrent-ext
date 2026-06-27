### Etapas para instalar plug-ins de pesquisa para qBittorrent versão 3.1.10 ou mais recente

0. Observe que plug-ins/scripts python não são, por natureza, considerados seguros. Portanto, qualquer uso de plug-ins não oficiais é por sua conta e risco. É uma boa prática auditar/dar uma olhada no plugin/script antes de instalar.

1. Acesse https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins
1. Na coluna `Download`, clique no link `Download` apropriado
1. Salve o arquivo `.py` em um local temporário em seu armazenamento local

1. Usando qBitTorrent
Usando a janela principal, clique em `Visualizar` -> `Mecanismo de pesquisa` para mostrar a guia de pesquisa
     ![screenshot](https://user-images.githubusercontent.com/14078661/51446055-a4431080-1cf3-11e9-8180-1994bdcbb672.png)
1. Vá para a `guia Pesquisar`
1. Clique no botão `Pesquisar plug-ins...`. Que está localizado no canto inferior direito.
1. A janela `Pesquisar plug-ins` será aberta. Ele mostra uma lista de plug-ins de mecanismos de pesquisa instalados.
1. Clique no botão `Instalar um novo` <br>
             ![screenshot](https://user-images.githubusercontent.com/14078661/51446120-bf625000-1cf4-11e9-98e1-b7e8b771c457.png))
1. A janela `Fonte do plugin` será aberta
1. Clique no botão `Arquivo local`
1. Navegue até o arquivo `.py` que você baixou na etapa acima. Selecione o arquivo `.py`.
1. Se for bem-sucedido, a seguinte mensagem será exibida
> O plugin do mecanismo de pesquisa <PLUGIN.NAME> foi instalado com sucesso.
1. Se não tiver sucesso, a seguinte mensagem será exibida
> O plug-in do mecanismo de pesquisa <PLUGIN.NAME> não pôde ser instalado.
1. Usando [esta página](https://github.com/qbittorrent/search-plugins/wiki/Unofficial-search-plugins) na coluna `Comment`, verifique se o seu sistema atende aos requisitos mínimos para cada plugin de pesquisa. Talvez o seu sistema atual não tenha os requisitos.
1. Clique no botão `Fechar`
1. Você pode excluir o arquivo `.py` do seu local temporário no armazenamento local, pois ele não é mais necessário.
1. Opcionalmente, você pode usar a janela `Pesquisar plug-ins` para ativar ou desativar plug-ins de pesquisa ou verificar se há atualizações.
1. Pronto. Você instalou com sucesso um novo plugin de pesquisa para qBittorrent.
