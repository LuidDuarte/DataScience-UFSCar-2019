from urllib.request import urlopen as uRec
from bs4 import BeautifulSoup as soup
from pymongo import MongoClient
import sys


def retorna_acoes_doc(url):
    uClient = uRec(url)
    page_html = uClient.read() # uCliente baixa tudo da url como um html puro 
    uClient.close()

    page_soup = soup(page_html, 'html.parser')

    campos_html = page_soup.findAll("th") #FindAll cria uma lista sendo os elementos as tags procuradas no ()
    nomes_campos = []
    for campo in campos_html:
        nomes_campos.append(campo.span.text) #Campo então, é uma tag 'th', dentro dela há um span, e então pegamos o texto dele

    todas_linhas = []
    corpo = page_soup.find("tbody") #Como tbody é um só, não há a necessidade de se usar o findAll 
    itens_corpo = corpo.findAll("tr") #Lista com todos tr que estão no tbody
    for linha in itens_corpo:
        tags_campos = linha.findAll("td") #Lista com todos td que estão em cada tr
        linha_especifica = {}
        if len(tags_campos) > 2: #Os dividendos são mostrados na mesma tabela, porém dentro do tr existem só 2 tds
            for tag in tags_campos: #Em cada td há um span com o valor que queremos
                linha_especifica[nomes_campos[tags_campos.index(tag)]] = tag.span.text
        else:
            linha_especifica['Date'] = tags_campos[0].span.text
            linha_especifica[tags_campos[1].span.text] = tags_campos[1].strong.text

        todas_linhas.append(linha_especifica) #adiciona esse dict em uma lista
    
    return todas_linhas

def insere_documento(collection,documento):

    collection.insert_many(documento) #insere a lista no banco


if __name__ == '__main__':
    url = ''
    if len(sys.argv) >= 2:
        n = 1
        while (n < len(sys.argv)):
            if(sys.argv[n] == '-h'):
                print('-url <url> ou -t <ticker>\n')
                quit()
            if(sys.argv[n] == '-url'):
                url = sys.argv[n+1]
            if(sys.argv[n] == '-t'):
                url_base = 'https://finance.yahoo.com/quote/'
                ticker = sys.argv[n+1].upper()
                url = url_base + ticker + '/history'

            n += 1

    if (url):
        #Conectar ao banco, escolhendo já a collection
        client = MongoClient('localhost', 27017)
        banco = client.TrabalhoBD
        acoes = banco.acoes

        insere_documento(acoes, retorna_acoes_doc(url))

        client.close()
    else:
        print("Erro na passagem de parametros\n")