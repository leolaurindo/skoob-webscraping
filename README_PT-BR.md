# Skoob Scraper

## Visão Geral

Este script faz login no [Skoob](https://www.skoob.com.br/), uma "rede social" brasileira para amantes de livros, e recupera os dados da estante do usuário em arquivos csv e planilha excel.

## Sobre este script

Este script surgiu quando uma amiga minha disse que estava tendo dificuldades para transferir os dados de seus livros para um caderno no Notion. Como eu estava estudando web scraping para o novo trabalho que consegui, aceitei o comentário como um desafio. No final, criei este script.

Ele já tem um ou dois meses e acredito que posso modularizar as tarefas em funções. Por preguiça, tentei fazer isso com o chatGPT, mas só piorou as coisas. Eventualmente vou fazer isso, mas por enquanto vou deixar como está. Você pode, claro, fazer as mudanças que quiser.

Por enquanto, ele usa selenium para interagir com os elementos da página web e seu html, bem como pandas para processar os dados recuperados em um formato dataframe.

## Instalação

Você pode executar o arquivo `setup_environment.bat` para configurar o ambiente ou seguir os passos abaixo:

Primeiro, clone o repositório para sua máquina local usando git clone

```
git clone https://github.com/leolaurindo/skoob-webscraping.git
```

Em seguida, instale os pacotes Python necessários

```
pip install -r requirements.txt
```

Você também precisará ter o google chrome instalado e o chrome-driver.exe para sua versão atual. Você pode baixar o Chrome na [página principal](https://www.google.com/intl/pt-BR/chrome/) e o driver [aqui](https://googlechromelabs.github.io/chrome-for-testing/)

## Configuração

O script usa config.json para gerenciar caminhos e senhas. Você pode substituir o config.json.sample pelas suas próprias credenciais e remover o formato sample.

## Executando o script

Navegue até o diretório clonado e execute a linha de comando

```
python main.py
```

# Licença

Você pode usá-lo como quiser.
