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

def define_diferencas(documento):
    print(documento)
    valor_anterior = float(documento['Values'][0]['Close*'])
    vetor_diferencas = []
    for i in range(1, len(documento['Values'])):
        if (documento['Values'][i].get('Close*')): #Usado get, para não dar erro em linhas que não há o close. 
            documento['Values'][i]['Variation']  = (float(documento['Values'][i]['Close*']) - valor_anterior )
            valor_anterior = float(documento['Values'][i]['Close*'])
    return documento

def insere_documento(collection,documento):
    documento = define_diferencas(documento)
    collection.insert(documento) #insere a lista no banco

if __name__ == '__main__':
    _url = False
    tags = []
    _ticker = False
    
    if len(sys.argv) >= 2:
        n = 1
        while (n < len(sys.argv)):
            if(sys.argv[n] == '-h'):
                print('-ticker <ticker> | -url "<url>" (opcional) | -tags <tags> (opcional)\n')
                quit()
            if(sys.argv[n] == '-ticker'):
                ticker = sys.argv[n+1].upper()
                _ticker = True
            if(sys.argv[n] == '-url'):
                url = sys.argv[n+1]
                _url = True
            if(sys.argv[n] == "-tags"):
                while(n < len(sys.argv)-1 and sys.argv[n+1][0] != '-'):
                    tags.append(sys.argv[n+1])
                    n += 1 
            n += 1

    if(not _ticker):
        print("Ticker inválido!\n")
        quit()

    if(not _url):
        url_base = 'https://finance.yahoo.com/quote/'
        url = url_base + ticker + '/history'
    
    
    #Conectar ao banco, escolhendo já a collection
    client = MongoClient('localhost', 27017)
    banco = client.TrabalhoBD
    acoes = banco.acoes

    acao = banco.acoes.find_one({"Ticker": ticker})
    
    if(acao):
        banco.acoes.update_one( {"_id": acao['_id']},
                                {"$set": {"Values":acao['Values'] + retorna_acoes_doc(url),
                                 "Tags":acao['Tags'] + tags}})
    else:
        documento = {}
        documento['Ticker'] = ticker
        documento['Tags'] = tags
        documento['Values'] = retorna_acoes_doc(url)

        insere_documento(acoes,documento) 

    client.close()