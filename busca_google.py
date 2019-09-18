import requests
from bs4 import BeautifulSoup as soup
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

def gera_url_pesquisa(data_inicio, data_fim, tags):
    qtd_tags = len(tags)-1
    string_tags = ''

    while(qtd_tags > 0):
        string_tags += tags[qtd_tags] + '+'
        qtd_tags -= 1
    string_tags += tags[0]

    url = 'https://www.google.com/search?tbs=cdr:1,cd_min:{},cd_max:{}&tbm=nws&q={}'.format(data_inicio, data_fim, string_tags)
    return url

def retorna_artigo(url):
    headers = requests.utils.default_headers() #Se não mudar o header, não tem permissão para acessar (httpError 403)
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
    })
    uClient = requests.get(url, headers)
    page_html = uClient.content
    uClient.close()

    page_soup = soup(page_html, 'html.parser')
    artigo_raw = page_soup.findAll('p')
    artigo = ''
    for paragrafo in artigo_raw:
        [script.extract() for script in paragrafo('script')] #tirar todas as tags scripts, porque o conteúdo interno é tido como texto também.
        artigo += paragrafo.text


    return artigo

def retorna_palavras_chaves(url):
    from nltk.corpus import stopwords #se não fizer a importação aqui, na segunda vez que a função é executada, da erro por stopwords ser um global (?)
    noticia = retorna_artigo(url)
    sentencas = sent_tokenize(noticia) #divide a noticia em sentenças 
    palavras = word_tokenize(noticia.lower()) #divide a noticia em palavras
    stopwords = set(stopwords.words('portuguese') + list(punctuation) + list(['``', '\'']))
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords] #da lista de palavras, retira as 'palavras vazias'
    
    return palavras_sem_stopwords

def retorna_buscas_doc(url):
    headers = requests.utils.default_headers() #Se não mudar o header, não tem permissão para acessar (httpError 403)
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36 OPR/63.0.3368.43',
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
        noticia['Link'] = noticia_raw.find('h3', {'class': 'r'}).a['href'][7:].split('&sa')[0] # os links começam com /url?q= antes do https:// no href
        fonte_data = (noticia_raw.find('div', {'class': 'slp'}).span.text).split(' - ')
        noticia['Fonte'] = fonte_data[0]
        noticia['Data'] = fonte_data[1]
        noticia['Palavras_Chaves'] = retorna_palavras_chaves(noticia['Link'])

        noticias.append(noticia)
    
    return noticias


print(retorna_buscas_doc('https://www.google.com.br/search?q=teste&client=opera&hs=vNW&sxsrf=ACYBGNTlSSjs4FnQOuvIO6UOjRDYUbY4og:1568787099491&source=lnms&tbm=nws&sa=X&ved=0ahUKEwjuhayu29nkAhXtGbkGHeLmDEIQ_AUIFCgE&biw=1920&bih=938'))