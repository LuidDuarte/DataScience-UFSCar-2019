from urllib.request import urlopen as uRec
from bs4 import BeautifulSoup as soup
from pymongo import MongoClient

#Conectar ao banco, escolhendo já a collection
client = MongoClient('localhost', 27017)
banco = client.TrabalhoDB
acoes = banco.acoes

my_url = 'https://finance.yahoo.com/quote/BUD/history?period1=1565924400&period2=1566356400&interval=1d&filter=history&frequency=1d'
uClient = uRec(my_url)
page_html = uClient.read() # uCliente baixa tudo da url como um html puro 
uClient.close()

page_soup = soup(page_html, "html.parser")

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
    for tag in tags_campos: #Em cada td há um span com o valor que queremos
        linha_especifica[nomes_campos[tags_campos.index(tag)]] = tag.span.text
    todas_linhas.append(linha_especifica) #adiciona esse dict em uma lista

acoes.insert_many(todas_linhas) #insere a lista no banco