import sys
from pymongo import MongoClient
from busca_google import retorna_doc_noticias

def retorna_pontos_criticos(acao):
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

def insere_pontos_criticos(acao):
        vetor_pontos = retorna_pontos_criticos(acao)
        pontos_criticos = []
        for ponto in vetor_pontos[0:3]:
                ponto['News'] = retorna_doc_noticias(ponto['Date'], acao['Tags'])
                pontos_criticos.append(ponto)

        banco.acoes.update(
                {"Ticker": ticker},
        {
                '$set': {"Critical_Points": pontos_criticos}
        }
        )



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
        insere_pontos_criticos(acao)
        