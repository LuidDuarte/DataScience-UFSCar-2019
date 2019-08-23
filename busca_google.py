from urllib.request import urlopen as uRec
from bs4 import BeautifulSoup as BeautifulSoup

def gera_url_pesquisa(data_inicio, data_fim, tags):
    qtd_tags = len(tags)-1
    string_tags = ''

    while(qtd_tags > 0):
        string_tags += tags[qtd_tags] + '+'
        qtd_tags -= 1
    string_tags += tags[0]

    url = 'https://www.google.com/search?tbs=cdr:1,cd_min:{},cd_max:{}&tbm=nws&q={}'.format(data_inicio, data_fim, string_tags)
    
    return url

