# - Título:
#       JSONs para DataFrame Pandas (2022)
# - Descrição:
#       Converte multiplos arquivos JSON criados pelo programa Publish and Perish e um único DataFrame Pandas
# - Autor:
#       Marlon Resende Faria
# - Orientador:
#       Alfredo Goldman vel Lejbman 

from glob import glob
import pandas as pd
import os
import re
import json
import codecs


# ------- Parametros para execução do programa  ------- #
base = 'gsprofile' # crossref | gsauthor | gscholar | gsciting | gsprofile | masv2 | pubmed | scopus | wos
prefixo = base + "_"
sufixo = '_2021'

local = os.path.dirname(os.path.abspath(__file__))                              # Caminho da pasta em que o aquivo PY está sendo executado

diretorio='\\dados\\json_pop'                                                   # Diretório onde estão os arquivos JSON criados pelo PoP
caminho = local + diretorio                                                     # Caminho completro para os arquivos

def extrair_nome(string: str, começo: str, fim: str) -> str:
    """
    Remove substrig entre dois caractere/substring

    Parameters
    ----------
    string : str
        String completa

    começo : str
        substring anterior a a subtring de interesse

    fim : str
        substring posterior a subtring de interesse

    Returns
    -------
    fim : str
        substring de interesse 
    """ 
    padrão = começo +"(.*)" + fim
    substring = re.search(padrão, string).group(1)
    return substring

def jsons_para_dataframes(caminho:str ,prefixo: str,sufixo: str):
    """
    Remove substrig entre dois caractere/substring

    Parameters
    ----------
    caminho : str
        String completa

    prefixo : str
        subtring prefixo anterior a a subtring de interesse

    sufixo : str
        substring sufixo posterior a subtring de interesse

    sufixo:
    -------
    fim : str
        substring de interesse 
    """ 
    print(caminho)
    lista_json = []                                                                     # lista vazia para armazenar os caminhos dos arquivos JSON  
    for arquivo in glob(caminho+"/*.json"):                                             # itera sob os arquivos JSON na pasta
        lista_json.append(arquivo)                                                      # adiciona o caminho na lista
    lista_dataframes = []                                                               # lista vazia para armazenar dados dos arquivos JSON
    for arquivo_json in lista_json:                                                     # itera sob a lista de caminhos dos arquivos JSON
        json_aberto=json.load(codecs.open(arquivo_json, 'r', 'utf-8-sig'))              # lê o arquivo JSON         
        a=pd.DataFrame(json_aberto)
        nome=extrair_nome(arquivo_json,prefixo,sufixo)                                  # Extrai no nome do pesquisador pelo nome do arquivo
        a['Nome'] = nome
        lista_dataframes.append(a)
    #print(lista_dataframes)
    df = pd.concat(lista_dataframes)                                                    # tranforma a lista de dados JSON em DataFrame Pandas
    df = df.reset_index(drop=True)                                                      # reinicia o índice do DataFrame
    return df

df=jsons_para_dataframes(caminho,prefixo,sufixo)
df.to_csv(local+'\\dados\\df_coletas\\df_BaseX.csv', index=False)
