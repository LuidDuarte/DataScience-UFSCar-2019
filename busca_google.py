from urllib.request import urlopen as uRec
from bs4 import BeautifulSoup as BeautifulSoup

class Pesquisa:
                        #mês-dia-ano4digitos
    def __init__(self, data_inicio, data_fim, tags):
        self.data_inicio = data_inicio.split('-')
        self.data_fim = data_fim.split('-')
        self.tags = []
        for tag in tags:
            self.tags.append(tag)

def pesquisar(data_inicio, data_fim, tags):
    data_inicio = data_inicio.split('-')
    data_fim = data_fim.split('-')
    qtd_tags = len(tags)-1
    string_tags = ''

    while(qtd_tags > 0):
        string_tags += tags[qtd_tags] + '+'
        qtd_tags -= 1
    string_tags += tags[0]

    url = 'https://www.google.com/search?q={}&tbs=cdr%3A1%2Ccd_min%3A{}%2F{}%2F{}%2Ccd_max%3A{}%2F{}%2F{}&tbm=nws'.format(string_tags,data_inicio[0],data_inicio[1],data_inicio[2],data_fim[0],data_fim[1],data_fim[2])


