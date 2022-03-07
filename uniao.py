# União dos dados DataFrames por meio do Record Linkage (2022)
# - Título:
#    União de DataFrames Pandas (2022)
# - Descrição:
#     Une dataframes sem chave relacional. 
#     Utiliza o Record Linkage que releciona os dados por correspondência aproximada.
# - Autor:
#      Marlon Resende Faria
# - Orientador:
#       Alfredo Goldman vel Lejbman 


#    -- ABREVIATURAS --
#
#     df: DataFrame Pandas
#     lt: Lattes
#     gs: Google Scholar
#     ma: Microsoft Academic
#     ws: Web of Science
#     sp: Scopus

# -------- Bibliotecas -------- #
import pandas as pd
import re
import numpy as np
import unidecode
import recordlinkage as rl
import warnings
import numpy as np
import os

            # omite avisos da biblioteca recordlinkage
warnings.filterwarnings("ignore", category=DeprecationWarning)                                        
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


# -------- Funções -------- #

def removeMultEspaços(string: str) -> str:
    """
    Remove espaços ectras entre as palavras
    
    Parameters
    ----------
    string : str
        string com multiplos espaços
        
    Returns
    -------
    string : str
        string com apenas um espaço entre palavras
    """
    string_arrumada =  re.sub(' +', ' ', string)
    return string_arrumada

def removeAcentos(string: str) -> str:
    """ 
    Remove acentuação das palavras

    Parameters
    ----------
    string : str
        palavra com acentos
        
    Returns
    -------
    número : int
        palavra sem acentos
    """
    string_arrumada = unidecode.unidecode(string)
    return string_arrumada

def processa_texto(df: pd.DataFrame, coluna: list) -> pd.DataFrame:
    """
    Aplica funções para limpeza de texto

    Parameters
    ----------
    DataFrame: pd.DataFrame
        Dataframe original

    Coluna: list
        Coluna que será aplicado o processamento
        
    Returns
    -------
    DataFrame: pd.DataFrame
        Dataframe processado
    """
    coluna=str(coluna)
    df[coluna] = df[coluna].apply(str.rstrip)                                       # remove espaços a direita em strings
    df[coluna] = df[coluna].apply(str.lower)                                        # strings em letas minúsculas
    df[coluna] = df[coluna].apply(str.lstrip)                                       # remove espaços a esqueda em strings
    df[coluna] = df[coluna].apply(removeAcentos)                                    # remove acentuação
    df[coluna] = df[coluna].apply(removeMultEspaços)                                # remove espaços multiplos: maior ou igual a 2
    return df


def primeiraLetra(df: pd.DataFrame, coluna: str, nome: str) -> pd.DataFrame:
    """
    Cria uma coluna com a primeira letra do texto de uma coluna do DataFrame
    
    Parameters
    ----------
    DataFrame: pd.DataFrame
        Dataframe original

    Coluna: list
        Coluna que será aplicada a função

    Nome: list
        Nome da nova coluna com 1ª letra      
    
    Returns
    -------
    DataFrame: pd.DataFrame
        Dataframe com 1ª letra
    """
    df[nome] = df[str(coluna)].astype(str).str[0]
    return df


def numeroAutores(string: str) -> int:
    """
    Calcula o nº de autores
 
    Parameters
    ----------
    string : str
        recebe lista de autores convertida como string
        
    Returns
    -------
    número : int
        número de autores da publicação
    """
    a = eval(string)
    n = len(a)
    return n


def primeiroAutor(string: str) -> str:
    """
    Devolve o primeiro elemento de uma lista de acordo com tipo (nome do 1ª autor)

    Parameters
    ----------
    string : str
        recebe lista de autores convertida como string
                
    Returns
    -------
    string : str
        Primeiro elemento da lista (1º Autor)
    """
    lista = eval(string)
    if len(lista)>0:
        primeiro = primeiroElemento(lista)
        if type(primeiro) == str:
            return primeiro
        elif type(primeiro)== dict:
            return primeiro['name']
        else:
            return "NA"
    else:
        return "NA"


def ultimoNome(string: str) -> str:
    """
    Devolve a última palavra de uma string (sobrenome)

    Parameters
    ----------
    string : str
        texto (nome completo)
        
    Returns
    -------
    string : str
        texto (sobrenome)
    """
    string = string.replace('.','').replace(',',' ').split(' ')[-1]
    return string


def primeiroElemento(lista: list) -> str:
    """
    Devolve primeiro elemento de uma string

    Parameters
    ----------
    lista : list
        lista de strings
        
    Returns
    -------
    string : str
        primeira string da lista
    """
    try:
        return lista[0]
    except:
        return 'NA'


def primeiroAutorWOS(string: str) -> str:
    """
    Devolve primeiro elemento de uma string (desenhada para coletar nome do 1º autor dos dados WoS)

    Parameters
    ----------
    string : list
        string cujos elementos estão separados por ponto-vírgula
        
    Returns
    -------
    string : str
        primeiro elemento da lista originada da string original
    """
    lista = string.split(';')
    pri_ele = primeiroElemento(lista)
    return pri_ele

# Nomes dos autores WoS começam pelo último nome e o separador é ;. Foi mais fácil criar funções específicas para estes casos. 
def ultimoNomeWOS(string: str) -> str:
    """
    Devolve ultima palavra de uma frase (sobrenome do autor nos dados WoS)

    Parameters
    ----------
    string : str
        string (nome completo)
        
    Returns
    -------
    string : str
        última palavra (sobrenome)
    """
    lista = string.split(',')
    ult_nome = primeiroElemento(lista)
    return ult_nome

def numeroAutorWOS(string: str) -> str:
    """
    Devolve primeiro elemento de uma string (desenhada para coletar nome do 1º autor dos dados WoS)

    Parameters
    ----------
    string : str
        lista de strings na convertida em string
        
    Returns
    -------
    string : str
        primeiro elemento da lista originada da string original
    """
    lista = string.split(';')
    numero_autores = len(lista)
    return numero_autores

def posicaoLattes(string: str) -> int:
    """
    Devolve um número dentro de uma lista escrita como string
    (Devolve a posição do autor ifusp dentro da publicação)

    Parameters
    ----------
    string : list
        lista de strings
        
    Returns
    -------
    número : int
        número (posição)
    """
    lista = eval(string)
    posicao = primeiroElemento(lista)
    return posicao

def renomearColunas(df: pd.DataFrame, dic: dict) -> pd.DataFrame:
    """
    Altera os texto do cabeçalho do DataFrame de acordo um dicionário

    Parameters
    ----------
    DataFrame : pd.DataFrame
        DataFrame com os dados
    
    dic : dict
        dicionário com os valores novos e antigos cabeçalhos 
    
    Returns
    -------
    DataFrame : pd.DataFrame
        DataFrame com novos cabeçalhos
    """
    df.columns=df.columns.str.lower() 
    df=df.rename(dic, axis='columns')
    return df

def filtraColunas(df: pd.DataFrame, colunas_interesse: list) -> pd.DataFrame:
    """
    Seleciona apenas as colunas de interesse de uma DataFrame

    Parameters
    ----------
    DataFrame : pd.DataFrame
        DataFrame para filtragem

    colunas_interesse : list
        lista com os cabeçalhos das colunas de interesse

    Returns
    -------
    DataFrame : pd.DataFrame
        DataFrame com as colunas filtradas
    """
    df = df[colunas_interesse]
    return df

def criarIndice(df: pd.DataFrame, tag: str) -> pd.DataFrame:
    """
    Cria um indice com uma tag para identificar o dataframe de origem dos dados

    Parameters
    ----------
    DataFrame : pd.DataFrame
        DataFrame

    tag : str
        Sufixo (string) que será usado como tag

    Returns
    -------
    DataFrame : pd.DataFrame
        DataFrame com tags no índice
    """    
    df['index'] = tag + df.index.astype(str)
    df = df.set_index('index') 
    return df

def ultimoNomeInvertido(string):
    """
    Devolve em ordem inversa palavras separadas por vírgula.
    Exemplo nome de autores: SOBRENOME, NOME -> NOME SOBRENOME

    Parameters
    ----------
    texto : str
        PALAVRA1, PALAVRA2

    Returns
    -------
    texto : str
        PALAVRA2 PALAVRA1
    """  
    if ',' in string:
        return string.split(',')[0]
    else:
        return string

def tagColuna(df: pd.DataFrame, tag: str, colunas: list = ['todos']) -> pd.DataFrame:
    """
    Adiciona tag aos cabeçalhos de colunas de DataFrame definidos.
    Caso os cabeçalhos não sejam declarados, todos receberam a tag.

    Parameters
    ----------
    DataFrame : pd.DataFrame
        DataFrame

    tag : str
        Sufixo (string) que será usado como tag
    
    colunas : list
        Colunas cujas cabeçalhos receberão tags
    Returns
    -------
    DataFrame : pd.DataFrame
        DataFrame com tags
    """  
    if colunas[0] == 'todos' :
        colunas = list(df.columns)
        df=df.rename(columns = dict(zip(colunas, [coluna + '_' + tag for coluna in colunas])))     
    else:
        df=df.rename(columns = dict(zip(colunas, [coluna + '_' + tag for coluna in colunas])))
    return df


def processaDF(df: pd.DataFrame, dic: dict, colunas: list, tag: str) -> pd.DataFrame:
    """
    Aplica diversas funções que processam os dados coletados nas plataformas

    Parameters
    ----------
    DataFrame : pd.DataFrame
        DataFrame

    dic : dict
        Dicionário com

    colunas : list
        Colunas que devolvidas no DataFrame final

    tag : str
        Sufixo (string) que será usado como tag
    
    colunas : list
        Colunas cujas cabeçalhos receberão tags
    Returns
    -------
    DataFrame : pd.DataFrame
        DataFrame com tags
    """    
    df = renomearColunas(df, dic)                                                           # Renomea os cabeçalhos das colunas                                          
    df = processa_texto(df,'titulo')                                                        # Limpa o texto dos títulos
    df['ano'].fillna('0', inplace = True)                                                   # Substitui os NA por 0 na coluna com "ano"
    df.fillna('[]', inplace = True)                                                         # Substitui os NA por '[]' em todas as colunas restantes
    df['n_autores'] = df['autores'].apply(numeroAutores)                                    # Devolve uma coluna com o número da publicação
    df['1_autor'] = df['autores'].apply(primeiroAutor)                                      # Devolve uma coluna com o 1º autor da publicação
    df['1_autor'] = df['1_autor'].apply(ultimoNomeInvertido)                                # Inverte os nomes apresentados na forma SOBRENOME, NOME
    df['ult_nome_1_autor'] = df['1_autor'].apply(ultimoNome)                                # Devolve uma coluna com o sobrenome (último nome) o 1º autor da publicação
    df['ano'] = df['ano'].astype(int)                                                       # Corrige problema de tipagem
    df = primeiraLetra(df,'titulo','1_letra')                                               # Devolve Dataframe com uma coluna com a 1ª letra dos títulos
    df = filtraColunas(df, colunas)                                                         # Devolve Dataframe apenas com as colunas de interesse
    df = criarIndice(df, tag)                                                               # Devolve Dataframe com novo índice com a tag definida
    return df

# para WOS, a melhor solução criar funções prórias para processar dados da WoS
def processaDFwos(df: pd.DataFrame, dic: dict, colunas: list, tag: str) -> pd.DataFrame:
    """
    Aplica diversas funções que processam os dados coletados nas plataformas

    Parameters
    ----------
    DataFrame : pd.DataFrame
        DataFrame

    dic : dict
        Dicionário com

    colunas : list
        Colunas que devolvidas no DataFrame final

    tag : str
        Sufixo (string) que será usado como tag
    
    colunas : list
        Colunas cujas cabeçalhos receberão tags
    Returns
    -------
    DataFrame : pd.DataFrame
        DataFrame com tags
    """
    df = renomearColunas(df,dic)                                                           # Renomea os cabeçalhos das colunas                                                              
    df = processa_texto(df,'titulo')                                                       # Limpa o texto dos títulos
    df['ano'] = df['ano'].fillna('0').astype(int)                                          # Corrige problema de tipagem
    df.fillna('[]', inplace=True)                                                          # Substitui os NA por '[]' em todas as colunas restantes
    df['n_autores'] = df['autores'].apply(numeroAutorWOS)                                  # Devolve uma coluna com o número da publicação (especial para WoS)
    df['1_autor'] = df['autores'].apply(primeiroAutorWOS)                                  # Devolve uma coluna com o 1º autor da publicação (especial para WoS)
    df['1_autor'] = df['1_autor'].apply(ultimoNomeInvertido)                               # Inverte os nomes apresentados na forma SOBRENOME, NOME
    df['ult_nome_1_autor'] = df['1_autor'].apply(ultimoNomeWOS)                            # Devolve uma coluna com o sobrenome (último nome) o 1º autor da publicação
    df = primeiraLetra(df,'titulo','1_letra')                                              # Devolve Dataframe com uma coluna com a 1ª letra dos títulos
    df = filtraColunas(df, colunas)                                                        # Devolve Dataframe apenas com as colunas de interesse
    df = criarIndice(df, tag)                                                              # Devolve Dataframe com novo índice com a tag definida
    return df

def RecordLinkage(dfA: pd.DataFrame, dfB: pd.DataFrame, candidatos: bool) -> pd.DataFrame:
    """
    Recebe dois DataFrames, seleciona candidatos e compara atributos: ano, título e sobrenome o 1º autor

    Parameters
    ----------
    dfA : pd.DataFrame
        Primeiro DataFrame 

    dfB : pd.DataFrame
        Segundo DataFrame        
        
    Returns
    -------
    features : pd.DataFrame
        DataFrame com índices e correspondências encontradas
    """
    indexador = rl.Index() 
    if candidatos ==  True:
        indexador.block('1_letra')                                                   # coluna/atributo em comum nos dois dataframes que será utilizada para seleção de candidatos
    else:
        indexador.full()                                                             # caso não selecione coluna/atributo canditato
    candidatos = indexador.index(dfA, dfB)                                           # dataframe com indices dos candidatos
    comparar = rl.Compare() 
    comparar.numeric('ano', 'ano', offset =1.0, label='ano')                         # Paramêtros para comparar "ano", com offset  1
    comparar.string('titulo', 'titulo', method='levenshtein',                        # Paramêtros parar compara "títulos"
                     threshold=0.8, label='titulo')                                 
    comparar.string('ult_nome_1_autor', 'ult_nome_1_autor', method='levenshtein',    # Paramêtros para comparar "nome do 1 autor"
                     threshold=0.8, label='ult_nome_1_autor')                       
    features = comparar.compute(candidatos, dfA, dfB)                                # Executa as comparações previamente configuradas
    return features

def selecaoCandidatos(df: pd.DataFrame, valor: int) -> pd.DataFrame:
    """
    Aplica diversas funções que processam os dados coletados nas plataformas

    Parameters
    ----------
    DataFrame : pd.DataFrame
        DataFrame com as correspondências encontradas entre dois DataFrames

    valor : int
        Número de correspondência mínima para seleção dos observações candidatas
    
    Returns
    -------
    DataFrame : pd.DataFrame
        DataFrame com os candidatos selecionados 
    """    
    return df[df.sum(axis=1)>=valor]                                                # Seleciona apenas os candidatos cuja soma de features seja igual ou maior que o valor

def unirDF(dfA: pd.DataFrame ,dfB: pd.DataFrame,df_candidato: pd.DataFrame,tag:str) -> pd.DataFrame:
    """
    Recebe dois DataFrames, seleciona candidatos e compara atributos: ano, título e sobrenome o 1º autor

    Parameters
    ----------
    dfA : pd.DataFrame
        Primeiro DataFrame utilizado na função RecordLikage()

    dfB : pd.DataFrame
        Segundo DataFrame utilizado na função RecordLikage()       
 
    df_candidato : pd.DataFrame
        DataFrame devolvido pela função RecordLikage()
    
    Returns
    -------
    features : pd.DataFrame
        DataFrame resultado da união de acordo com os candidatos selecionados
    """   
    candidatos = selecaoCandidatos(df_candidato, 3)                                  # Seleciona candidatos
    dfA = dfA.reset_index()                                                          # resta/transforma o indice em um coluna do dataframe
    dfB = dfB.reset_index()                                                          # idem acima
    candidatos = candidatos.reset_index()                                            # idem acima
    dfA = dfA.rename(columns={'index':'index_1','n_autores':'n_autores_lt'})         # renomeia o coluna/índice de acordo com o que existe no DF candidatos
    dfB = dfB.rename(columns={'index':'index_2'})
    dfA['index_1'] = dfA['index_1'].astype(str)                                      # resolve problema de tipagem
    dfB['index_2'] = dfB['index_2'].astype(str)                                      # idem acima
    df_unido = pd.merge(candidatos[['index_1','index_2']], dfA, on='index_1')        # une o DF de candidatos com os dados do df_lattes pelo índice index_1
    df_unido = df_unido.merge(dfB[['index_2','citacoes','n_autores']], how='left')   # une ao dataframe df_unido os dados bibliograficos: citações e nº de autores
    df_unido = tagColuna(df_unido,tag,['citacoes','n_autores'])
    return df_unido


#-------- Dicionário de tradução das colunas-----#
nomes_colunas={'180 day usage count': 'contagem_uso_180_dias',
 'abstract': 'resumo',
 'addresses': 'endereço',
 'article number': 'numero_artigo',
 'article title': 'titulo',
 'article_url': 'url_artigo',
 'atualiza.': 'atualizacao',
 'author full names': 'nome_completo_autores',
 'author keywords': 'palavras-chave_autor',
 'authors': 'autores',
 'author': 'autores',
 'book author full names': 'livro_nome_completo_autores',
 'book authors': 'livro_autores',
 'book doi': 'doi_livro',
 'book editors': 'livros_editora',
 'book group authors': 'livro_grupo_autores',
 'book series subtitle': 'subtitulo_serie_livros',
 'book series title': 'titulo_serie_livros',
 'citation_url': 'url_citacoes',
 'cited reference count': 'contagem_referencias_citadas',
 'cited references': 'referencias_citadas',
 'cites': 'citacoes',
 'conference date': 'conferencia_data',
 'conference host': 'conferencia_anfitriao',
 'conference location': 'conferencia_localização',
 'conference sponsor': 'conferencia_patrocinador',
 'conference title': 'conferencia_titulo',
 'date of export': 'data_exportacao',
 'document type': 'tipo_documento',
 'doi': 'doi',
 'early access date': 'data_acesso_antecipado',
 'eissn': 'ISSN',
 'email addresses': 'email',
 'endpage': 'pagina_final',
 'fulltext_url': 'url_texto_completo',
 'funding orgs': 'finaciadores',
 'funding text': 'texto_financiador',
 'group authors': 'grupo_autores',
 'highly cited status': 'fortemente_citado',
 'hot paper status': 'alta_taxa_citacao',
 'id': 'id_lattes',
 'ids number': 'number_ids',
 'isbn': 'ISBN',
 'issn': 'ISSN',
 'issue': 'edicao',
 'journal abbreviation': 'abreviacao_periodico',
 'journal iso abbreviation': 'abreviacao_ISO_periodico',
 'keywords plus': 'mais_palavras-chave',
 'lang': 'lingua',
 'language': 'lingua',
 'meeting abstract': 'resumo_conferencia',
 'name': 'nome_autor',
 'number of pages': 'numero_livro',
 'open access designations': 'acesso',
 'orcids': 'ORCID',
 'order': 'ordenacao',
 'order_ok': 'posição_ordem',
 'part number': 'numero_peca',
 'publication date': 'data',
 'publication type': 'tipo',
 'publication year': 'ano',
 'publisher': 'editora',
 'publisher address': 'endereço_editora',
 'publisher city': 'cidade_editora',
 'pubmed id': 'pubmed_id',
 'reprint addresses': 'endereço_reimpressao',
 'research areas': 'area_pesquisa',
 'researcher ids': 'researcher_id',
 'since 2013 usage count': 'contagem_uso_desde_2013',
 'source': 'fonte',
 'source title': 'fonte_titulo',
 'special issue': 'edicao_especial',
 'startpage': 'pagina_inicial',
 'supplement': 'suplemento',
 'times cited, all databases': 'citacoes',                          # tradução seria:'citacoes_todas_bases'. Para efeitos práticos essa coluna recebe o mesmo nome dos outros dataframes
 'times cited, wos core': 'citacoes_base_wos',
 'title': 'titulo',
 'type': 'tipo',
 'ut (unique wos id)': 'wos_id',
 'wos categories': 'categoria_wos',
 'year': 'ano',
 'order_ok':'posicao',
 'nome_complt':'autor_ifusp',
  }
 

local = os.path.dirname(os.path.abspath(__file__))                 # Caminho da pasta em que o pop.py está sendo executado

colunas = ['autores','titulo','ano','citacoes','n_autores',
            '1_autor','ult_nome_1_autor','1_letra']

colunas_lattes = ['autores','titulo','ano','n_autores','1_autor',  # lattes não tem citações
                'ult_nome_1_autor','1_letra','lingua','posicao',
                'autor_ifusp']

            # Carrega os os dataframes com os dados das plataformas
df_lattes = pd.read_csv(local + '\dados\coletas\df_lattes.csv')
df_msacd = pd.read_csv(local + '\dados\coletas\df_msacd.csv')
df_scholar = pd.read_csv(local + '\dados\coletas\df_scholar.csv')
df_scopus = pd.read_csv(local + '\dados\coletas\df_scopus.csv')
df_wos = pd.read_csv(local + '\dados\coletas\df_wos.csv')

print('Etapa 1/6: DataFrames carregados')

            # processa os dados das plataformas: limpeza, criação de novas variáveis,
            # adição de tags no cabeçalhos
df_lattes_ = processaDF(df_lattes, nomes_colunas, colunas_lattes, 'lt')
df_msacd_ = processaDF(df_msacd, nomes_colunas, colunas, 'ma')
df_scholar_ = processaDF(df_scholar, nomes_colunas, colunas, 'gs')
df_scopus_ = processaDF(df_scopus, nomes_colunas, colunas, 'sp')
df_wos_ = processaDFwos(df_wos, nomes_colunas, colunas, 'ws')

print('Etapa 2/6: DataFrames limpos')

print('Etapa 3/6: Selecionando candidatos - pode levar algum tempo')

            # Executa a busca por candidatos e computa as comparações de título, ano e sobrenome do último autor
df_lt_ma = RecordLinkage(df_lattes_,df_msacd_, True)
df_lt_sp = RecordLinkage(df_lattes_,df_scopus_, True)
df_lt_gs = RecordLinkage(df_lattes_,df_scholar_, True)
df_lt_ws = RecordLinkage(df_lattes_,df_wos_, True)

print('Etapa 3/6: Candidatos selecionados')

            # Após selecionados os candidatos, executa a únião dos conjuntos
df_lt_gs = unirDF(df_lattes_,df_scholar_, df_lt_gs,'gs')
df_lt_ma = unirDF(df_lattes_,df_msacd_, df_lt_ma,'ma')
df_lt_sp = unirDF(df_lattes_,df_scopus_, df_lt_sp,'sp')
df_lt_ws = unirDF(df_lattes_,df_wos_, df_lt_ws,'ws')

print('Etapa 4/6: unindo DataFrames')

            # Concatena todos os dataframes verticalmente
df = pd.concat([
                df_lt_gs,
                df_lt_ma,
                df_lt_sp,
                df_lt_ws])

            # acerta a variável posição do autor dentro da lista convertida em string
df['posicao'] = df.posicao.apply(posicaoLattes)

            # Agrupa os dados por título e autor ifusp. Assim se elimina duplicatas de publicações encontradas em 2 ou mais dataframes
            # Publicações com dois autores ifusp não podem ser agrupadas pois prejudicaria um dos autores no cálculo das métricas
            # O resultado será uma linha por publicação/autor ifusp
df_= df.groupby(['titulo','autor_ifusp'], as_index=False)[['index_1',
                        'ano',
                        'posicao',
                        'citacoes_ma',
                        'citacoes_gs',
                        'citacoes_ws',
                        'citacoes_sp',
                        'n_autores_lt',
                        'n_autores_gs',
                        'n_autores_ma',
                        'n_autores_sp',
                        'n_autores_ws',
                        'autores',
                        'autor_ifusp'
                        ]].first().reset_index()

            # Seleciona maior valor de "nº de autores" obtido das bases
df_['n_autores'] = df_[['n_autores_ws',
                    'n_autores_sp',
                    'n_autores_lt',
                    'n_autores_ma',
                    'n_autores_gs'
                    ]].astype(float).max(axis=1)
            # Seleciona maior valor de "ctiações" obtido das bases 

df_['citacoes'] = df_[['citacoes_ws',
                    'citacoes_sp',
                    'citacoes_gs',
                    'citacoes_ma'
                    ]].astype(float).max(axis=1)

print('Etapa 5/6: DataFrames unidos')


            # Seleciona apenas as variáveis de interesse
df_ = df_[['index_1', 'titulo','ano','posicao','citacoes','n_autores','autores','autor_ifusp']]
df_.to_csv(local + '\dados\dados_consolidados\df_consolidado.csv')

print('Etapa 6/6: DataFrame consolidado salvo na pasta: dados\dados_consolidados\df_consolidado.csv')
