RUNTIME PLANTA BAIXA DA FÁBRICA EM TEMPO REAL


- API backend que consulta dados de uma fonte API WEB e junta com outra fonte utilizando web scraping com Python Selenium (dados de uma página), essa coleta ocorre num loop a cada 10 segundos e escreve num arquivo JSON numa pasta de rede

- O servidor python começa a rodar no host 8000 e lê essa API JSON na pasta de rede e escreve num endpoint

- O HTML junto com o Javascript faz um get dos dados do endpoint dentro de um loop, e passa por cada DIV e compara com cada objeto do JSON para mudar as cores de acordo com as informações contidas
