import requests
from bs4 import BeautifulSoup as soup

def gera_url_pesquisa(data_inicio, data_fim, tags):
    qtd_tags = len(tags)-1
    string_tags = ''

    while(qtd_tags > 0):
        string_tags += tags[qtd_tags] + '+'
        qtd_tags -= 1
    string_tags += tags[0]

    url = 'https://www.google.com/search?tbs=cdr:1,cd_min:{},cd_max:{}&tbm=nws&q={}'.format(data_inicio, data_fim, string_tags)
    
    return url

def retorna_buscas_doc(url):
    headers = requests.utils.default_headers() #Se não mudar o header, não tem permissão para acessar (httpError 403)
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })
    uClient = requests.get(url, headers)
    page_html = uClient.content
    uClient.close()

    page_soup = soup(page_html, 'html.parser')

    noticias_raw = page_soup.findAll('div', {'class': 'g'})
    noticias = []

    for noticia_raw in noticias_raw:
        noticia = {}
        noticia['Manchete'] = noticia_raw.find('h3', {'class': 'r'}).a.text
        noticia['Link'] = noticia_raw.find('h3', {'class': 'r'}).a['href'][7:] # os links começam com /url?q= antes do https:// no href
        fonte_data = (noticia_raw.find('div', {'class': 'slp'}).span.text).split(' - ')
        print(fonte_data)
        noticia['Fonte'] = fonte_data[0]
        noticia['Data'] = fonte_data[1]
        noticias.append(noticia)

    print(noticias[:1])

url = 'https://www.google.com/search?tbs=cdr:1,cd_min:08/01/2019,cd_max:08/26/2019&tbm=nws&q=batatais'
retorna_buscas_doc(url)