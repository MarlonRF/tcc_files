# - Título:
#    União de DataFrames Pandas (2022)
# - Descrição:
#     Executa diversas buscas no programa Publish or Perish por linhas de comando.
#     É necessária um tabela com nome e IDs dos pesquisadores para criar os comandos de busca. 
#     É necessário instalar o programa Publish and Perish, nas versões padrão e linha de comando (CLI)
#     Parte do trabalho de conclusão de curso de Bacharelado em Matemática Aplicada e Computaicional do IME/USP.
# - Autor:
#      Marlon Resende Faria
# - Orientador:
#       Alfredo Goldman vel Lejbman 



# Execução em laço do programa Publish and Perish - versão CLI (2022)
# Autor: Marlon Resende Faria
# Parte do trabalho de conclusão de curso de Bacharelado em Matemática Aplicada e Computaicional do IME/USP
# É necessário instalar o programa Publish and Perish, nas versões padrão e linha de comando (CLI)


# -------- Bibliotecas -------- #
import os
import pandas as pd
from datetime import datetime
import time
# -------- Parametro para execução dos comandos--------#
programa='pop7query'                                    # mudar de versão se necessário
manter_fechar='/K'                                      # /K # Janea do prompt - "Close" ou "Keep"
programa='pop7query'                                    # mudar de versão se necessário
base="gsprofile"                                        # crossref | gsauthor | gscholar | gsciting | gsprofile | masv2 | pubmed | scopus | wos
coluna_identificador = "Identificador Scholar"          # cabeçalho da coluna da tabela com os ID da base
chave="author"                                          # pode-se realizar busca por outras chaves, como título do arquivo
salvar='.json'                                          # .csv | .json | .rtf | .tsv
espera = 5                                              # em segundos .Tempo de espera para realizar para próxima busca. Evita ser bloqueado
# ID="XXXXXXX"                                          # inserido via arquivo csv
# nome_arquivo = "XXXXXXX"                              # inserido via arquivo csv

def buscarPoP(ID: str, chave: str, base_dados: str, nome: str, salvar_como: str)-> None:
    manter_fechar = '/C'                                                            # ou /K
    programa = 'pop7query'                                                          # pop CLI - altere caso utilize outra versão
    chave = str(chave)                                                              # tipo de chave de busca
    ID = str(ID)                                                                    # ID do pesquisador
    base_dados = str(base_dados)                                                    # Base de dados bibliográficos
    salvar_como = str(salvar_como)                                                  # Formato de arquivo dos dados
    data=datetime.today().strftime("%Y_%m_%d")                                      # Data da coleta
    nome_arquivo= base_dados +'_'+ nome.replace(' ','_') + '_' + data + salvar_como # Nome do arquivo: base, nome do pesquisador, data e formato
    # Une os parametros e informações sobre arquivo num único comando
    comando = "start cmd" + manter_fechar +' '+  programa +' --'+ chave +'='+ '"'+ ID +'" --'+ base_dados +' '+ nome_arquivo
    raw_s = r'{}'.format(comando)                                                   # Converte toda string em raw string
    os.system(raw_s)                                                                # Aplica o comando
#start cmd /C popyquery --author =" fulano"

def buscaLaco(df: pd.DataFrame, base:str , identificador: str, espera: int=10 ) -> list:
    lista_por_id=[] 
    lista_por_nome=[]
    for indice, linha in df.iterrows():                          
        print("coletando dados de "+  linha['Nome'] + '  na base de dados '+ base)
        time.sleep(espera)                                                           # intevalo entre as buscas. Evita que bloqueio
        if linha[identificador]!="Não disponível":                                   # Filtra as linhas sem indentificadores
            buscarPoP(linha[identificador], 'author', base, linha['Nome'], '.json')  # Aplica o comando com os dados do pesquisador
            lista_por_id.append(linha['Nome'])
        else:
            print(linha['Nome'])#
            buscarPoP(linha['Nome'], 'author', base, linha['Nome'], '.json')
            lista_por_nome.append(linha['Nome'])
    print("-- Execução da lista finalizada --")
    # return lista_por_id, lista_por_nome

local = os.path.dirname(os.path.abspath(__file__))                                   # Caminho da pasta em que o pop.py está sendo executado
os.chdir(local+'\pop_cli')                                                           # Muda o diretório para execução do prompt
df = pd.read_excel(local + "\\dados\\listaID.xlsx")                                  # Abre a lista com ID dos pesquisadores
df_id = df[df[coluna_identificador]=='Não disponível']                                
lista_nomes = df_id['Nome']
buscaLaco(df_id, base, coluna_identificador, espera)                                 # Executa em laço os comandos para buscas via pop CLI

print("- Busca completa realizada - ")