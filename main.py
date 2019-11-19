import sys
from pymongo import MongoClient
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
#nltk.download('wordnet') 
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas


def retorna_lista_palavras(acao):
    critical_points = acao['Critical_Points']
    palavras_crescente = []
    palavras_decrescente = []

    for critical_point in critical_points:
        if critical_point['Crescente']:
            for noticia in critical_point['News']:
                palavras_crescente += noticia['Palavras_Chaves']
        else:
            for noticia in critical_point['News']:
                palavras_decrescente += noticia['Palavras_Chaves']

    return palavras_crescente,palavras_decrescente

#Most frequently occuring words
def get_top_n_words(corpus, n=None):
    vec = CountVectorizer().fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in      
                   vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                       reverse=True)
    return words_freq[:n]

#Most frequently occuring Bi-grams
def get_top_n2_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(2,2),  
            max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]

#Most frequently occuring Tri-grams
def get_top_n3_words(corpus, n=None):
    vec1 = CountVectorizer(ngram_range=(3,3), 
           max_features=2000).fit(corpus)
    bag_of_words = vec1.transform(corpus)
    sum_words = bag_of_words.sum(axis=0) 
    words_freq = [(word, sum_words[0, idx]) for word, idx in     
                  vec1.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], 
                reverse=True)
    return words_freq[:n]    

def imagem_palavras(palavras, nome):
    corpus = []
    ##Stemming
    ps=PorterStemmer()
    #Lemmatisation  
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in palavras] 
    text = " ".join(text)
    corpus.append(text)

    #Word cloud
    from os import path
    from PIL import Image
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
    import matplotlib.pyplot as plt
    wordcloud = WordCloud(
                            background_color='white',
                            max_words=100,
                            max_font_size=50, 
                            random_state=42
                            ).generate(str(corpus))
    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()
    fig.savefig(nome +'.png', dpi=1080)


    top_words = get_top_n_words(corpus, n=20)
    top_df = pandas.DataFrame(top_words)
    top_df.columns=["Word", "Freq"]

    top2_words = get_top_n2_words(corpus, n=20)
    top2_df = pandas.DataFrame(top2_words)
    top2_df.columns=["Bi-gram", "Freq"]
    print(top2_df)

    top3_words = get_top_n3_words(corpus, n=20)
    top3_df = pandas.DataFrame(top3_words)
    top3_df.columns=["Tri-gram", "Freq"]
    print(top3_df)





if __name__ == '__main__':
        _ticker = False

        if len(sys.argv) >= 2:
                n = 1
                while (n < len(sys.argv)):
                        if (sys.argv[n] == '-h'):
                                print('-ticker <ticker>\n')
                                quit()
                        if (sys.argv[n] == '-ticker'):
                                ticker = sys.argv[n+1].upper()

                                _ticker = True
                        n += 1

        if not _ticker:
                quit()
        
        client = MongoClient('localhost', 27017)
        banco = client.TrabalhoBD
        acoes = banco.acoes
        acao = banco.acoes.find_one({"Ticker": ticker})


        crescente, decrescente = retorna_lista_palavras(acao)
        imagem_palavras(crescente, 'crescente')
        imagem_palavras(decrescente, 'decrescente')
        
    
        