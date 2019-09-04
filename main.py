import sys
from pymongo import MongoClient

def retorna_pontos_criticos(ticker):
        client = MongoClient('localhost', 27017)
        banco = client.TrabalhoBD
        acoes = banco.acoes
        acao = banco.acoes.find_one({"Ticker": ticker})

        vetor_pontos = []
        for i in range(1, len(acao['Values'])):
                ponto = {}
                if(acao['Values'][i].get('Variation')):
                        if(abs(acao['Values'][i].get('Variation')) > (acao['Average'] + acao['Variancy'])):
                                ponto['Date'] = (acao['Values'][i]['Date'])
                                if acao['Values'][i]['Variation'] > 0:
                                        ponto['Crescente'] = 1 #Qual melhor nome para o campo?
                                else:
                                        ponto['Crescente'] = 0

                                vetor_pontos.append(ponto)
        client.close()
        return vetor_pontos

