import pandas as pd
import os 


def totalLinhas(df, query_txt:str='index == index'):
    """ Devolve o total de linhas do dataframe 
    """
    df=df.query(query_txt)
    n, _ = df.shape
    return n

def somaColuna(df, coluna:str, query_txt:str='index == index'):
    """ Devolve o soma de valores de uma coluna do DataFrame 
    """
    df=df.query(query_txt)
    return df[coluna].sum()

def media( numerador:int,denominador:int):
    """ Devolve média. Para ser usada em Dataframe por meio do método apply()
    """
    return numerador/denominador

def citacaoPorArtigo(df, query_txt, coluna_citacoes):
    """ Devolve número de citações por artigo
     """
    df = df.query(query_txt)
    n, _ = df.shape
    return df[coluna_citacoes].sum()/n

def mediaColuna(df, query_txt, coluna):
    """ Devolve o valor médio de uma coluna do DataFrame
     """
    df = df.query(query_txt)
    return df[coluna].mean()

def idadePublicacao(ano_publicacao:int,ano_atual:int):
    """ Devolve a idade de uma publicação de acordo com o ano_atual.
        Caso o ano_atual seja o mesmo do ano_publicação, devolve 1.
     """
    idade = ano_atual-ano_publicacao
    if idade==0:
        idade=1
    else:
        pass
    return idade

def hIndex(df, query_txt, coluna_citacoes:str):
    """ Calcula hm
    """
    df = df.query(query_txt).sort_values(by=[coluna_citacoes],ascending=False)
    df = df.reset_index(drop=True)
    df.index+= 1 
    df['ordem'] = [n for n in range(1, len(df)+1)]
    df['corte'] = abs(df[coluna_citacoes] - df['ordem'])
    return df['corte'].idxmin()

def hIIndex(df, query_txt, coluna_citacoes:str, coluna_n_autores:str):
  """ Calcula índice hI
  """
  df = df.query(query_txt).sort_values(by=[coluna_citacoes],ascending=False)
  df = df.reset_index(drop=True)
  df.index+= 1 
  df['ordem'] = [n for n in range(1, len(df)+1)]
  df['corte'] = abs(df['citacoes'] - df['ordem'])
  h_index= df['corte'].idxmin()
  df_hpapers = df[:h_index] # h-papers (papers cuja posição na tabela é >= h-index)
  N_a = df_hpapers['n_autores'].mean() # Média de autores do h-papers
  h_I =  h_index / N_a 
  return h_I

def gIndex(df, query_txt, coluna_citacoes:str):
  """Calcula índice g"""
  df = df.query(query_txt).sort_values(by=[coluna_citacoes],ascending=False)
  df = df.reset_index(drop=True)
  df.index+= 1 
  df['g^2'] = df.index**2
  df['citações acumuladas'] = df[coluna_citacoes].cumsum()
  df['corte'] = abs(df['g^2'] - df['citações acumuladas'])
  posicao_g = df['corte'].idxmin()
  return df.loc[posicao_g]['g^2']

def iIndex(df, i:int, coluna_citacoes:str, query_txt:str='index == index'):
    """ Devolve o total de linhas de uma dataframe """
    df=df.query(query_txt)
    df=df[df[coluna_citacoes]>=i]
    n, _ = df.shape
    return n

def hFracIndex(df, query_txt, coluna_citacoes:str, coluna_autores:str):
    """Calcula h-frac"""
    df = df.query(query_txt)[[coluna_citacoes, coluna_autores, ]]
    df['c/a'] = df[coluna_citacoes]/df[coluna_autores]
    df = df.sort_values(by=['c/a'],ascending=False) 
    df = df.reset_index(drop=True)
    df.index+= 1 
    df['corte'] = abs(df.index - df['c/a'])
    return df['corte'].idxmin()

def hIaIndex(df, query_txt, coluna_citacoes:str, coluna_autores:str, ano:int ):
    """Calcula h-frac"""
    df = df.query(query_txt)[[coluna_citacoes, coluna_autores, 'ano']]
    df['c/a'] = df[coluna_citacoes]/df[coluna_autores]
    df = df.sort_values(by=['c/a'],ascending=False)
    df = df.reset_index(drop=True)
    df.index+=1
    df['idade'] = df['ano'].apply(idadePublicacao, ano_atual=ano)
    idade_carreira = df['idade'].max()
    df['corte'] = abs(df.index - df['c/a'] )
    hI_norm = df['corte'].idxmin()
    hIa = hI_norm/idade_carreira
    return  hIa
    
def hmIndex(df, query_txt, coluna_citacoes:str, coluna_n_autores:str):
    """Calcula hm"""
  
    df = df.query(query_txt).sort_values(by=[coluna_citacoes],ascending=False)
    df = df.reset_index(drop=True)
    df.index+=1
    df['pesos'] = 1 / df[coluna_n_autores]
    df = df.sort_values(by = [coluna_citacoes], ascending=False)
    df['peso_acumulado'] = df['pesos'].cumsum()
    df['corte'] = abs(df[coluna_citacoes] - df['peso_acumulado'])
    posicao_hm = df['corte'].idxmin()
    return df.loc[posicao_hm][coluna_citacoes]


local = os.path.dirname(os.path.abspath(__file__))                                              # Caminho da pasta em que o aquivo PY está sendo executado
df =  pd.read_csv(local + '\dados\dados_consolidados\df_consolidado.csv')

ano_atual = 2021                                                                                # Paramêtro para calcular a idade das publicações

df['idade_publicacao'] = df.apply(lambda linha: idadePublicacao(linha['ano'], ano_atual), axis = 1)  # Média de citações ao ano de cada publicação          
df['media_citacoes_publicacao'] = df.apply(                                                     
                                           lambda linha: media(  
                                           linha['citacoes'],linha['idade_publicacao']), axis = 1)

nomes = df['autor_ifusp'].unique()                                                              # Armazena os nomes de todos os autores ifusp do DataFrame
querys_nomes = ['autor_ifusp=="'+nome+'"' for nome in nomes]                                    # Cria e armazena as texto das consultas que serão executadas por autor ifusp

            # Abaixo todas as métricas de cada autor ifusp no DataFrame são calculadas e armazenadas em listas

h_index = [hIndex(df,query,'citacoes') for query in querys_nomes]                               # Calcula e armazena o índice h
g_index = [gIndex(df,query,'citacoes') for query in querys_nomes]                               # Calcula e armazena o índice g 
hm_indice = [hmIndex(df,query,'citacoes','n_autores') for query in querys_nomes]                # Calcula e armazena o índice hm 
hI_indice = [hIIndex(df,query,'citacoes','n_autores') for query in querys_nomes]                # Calcula e armazena o índice hI 
citacoes = [somaColuna(df,'citacoes', query) for query in querys_nomes]                         # Calcula e armazena o número total de citações
total_artigos = [totalLinhas(df,query) for query in querys_nomes]                               # Calcula e armazena o número total de artigos
h_frac = [hFracIndex(df,query,'citacoes','n_autores') for query in querys_nomes]                # Calcula e armazena o índice h-frac 
hIa = [hIaIndex(df,query,'citacoes','n_autores',ano_atual) for query in querys_nomes]           # Calcula e armazena o índice hIa
i_index_10 = [iIndex(df, 10, 'citacoes', query) for query in querys_nomes]                      # Calcula e armazena o índice i10
i_index_25 = [iIndex(df, 25, 'citacoes', query) for query in querys_nomes]                      # Calcula e armazena o índice i25
i_index_50 = [iIndex(df, 50, 'citacoes', query) for query in querys_nomes]                      # Calcula e armazena o índice i50
i_index_100 =[iIndex(df, 100, 'citacoes', query) for query in querys_nomes]                     # Calcula e armazena o índice i100
media_cit_ano =  [mediaColuna(df, query, 'media_citacoes_publicacao') for query in querys_nomes]# Calcula e armazena a média de citações por artigo e por ano 
cit_p_arti = [citacaoPorArtigo(df, query, 'citacoes') for query in querys_nomes]                # Calcula e armazena a média de citações por arigo
media_autores =  [mediaColuna(df, query, 'n_autores') for query in querys_nomes]                # Calcula e armazena o índice de autores (incluindo o autor ifusp)
media_coautores = [media-1 for media in media_autores]                                          # Calcula e armazena o índice de coautores

            # Armazena as listas com os valores das métricas em um dicionário
data = {'Nomes':nomes,
        'índice h':h_index,
        'índice g':g_index,
        'índice hm':hm_indice,
        'índice hI':hI_indice,
        'total de citacoes':citacoes,
        'total de artigos':total_artigos,
        'índice i10':i_index_10,
        'índice i25':i_index_25,
        'índice i50':i_index_50,
        'índice i100':i_index_100,
        'índice hfrac':h_frac,
        'índice hIa':hIa,
        'citações por artigo':cit_p_arti,
        'média de citações por ano':media_cit_ano,
        'média de coautores':media_coautores
        }

        # Converte o dicionário Python em DataFrame pandas
df_= pd.DataFrame(data)
        
        #Salva o DataFrame em arquivo CSV
df_.to_csv(local + '\\dados\\df_metricas2.csv', index=False)
df_.to_excel(local + '\\dados\\df_metricas2.xls')