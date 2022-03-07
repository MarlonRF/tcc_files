# - Título: 
#     Parser XML Lattes
# - Descrição:
#     Converte dados dos XML, baixados dos currículos Lattes, em DataFrames Pandas.
#     Parte do trabalho de conclusão de curso de Bacharelado em Matemática Aplicada e Computaicional do IME/USP.
# - Autor:
#      Marlon Resende Faria
# - Orientador:
#       Alfredo Goldman vel Lejbman 



# -------- Bibliotecas -------- #
import os
import zipfile
import numpy as np
import pandas as pd
from glob import glob
import xml.etree.ElementTree as ET
from lxml import etree
import collections, re

# -------- Funções -------- #
def listarArquivos(diretorio: str="padrão", extensao: str="zip") -> list:
  """
  Adiciona tag aos cabeçalhos de colunas de DataFrame definidos.
  Caso os cabeçalhos não sejam declarados, todos receberam a tag.

  Parameters
  ----------
  diretorio : str
      Caminho até o diretório em que estão os arquivos ZIP/XML
      Por padrão é a pasta "\dados\xml_zip" relativo ao arquivo

  extensao : str
      Sufixo (string) que será usado como tag

  Returns
  -------
  lista
      lista com os caminhos para arquivos da extensão definida
  """ 
  lista = []
  if diretorio =="padrão":
    diretorio = os.path.dirname(os.path.abspath(__file__)) +'\\dados\\xml_zip' 
  else:
    pass
  padrão   = "*."+extensao
  for dir,_,_ in os.walk(diretorio):
      lista.extend(glob(os.path.join(dir,padrão)))
  return lista

def abreZip(arquivo: str='', diretorio_temp=: str='\\dados\\xml_zip\\temp') -> None:
  """
  Abre os arquios ZIP e extrai o arquivo curriculo.XML para diretório definido

  Parameters
  ----------
  arquivo : str
      Caminho do arquivo ZIP

  diretorio_temp : str
      Diretorio onde será salvo o XML extraido

  Returns
  -------
  None:
     Não devolve nada
  """ 
  diretorio_temp = os.path.dirname(os.path.abspath(__file__)) +diretorio_temp
  print(diretorio_temp)
  # with garante que um arquivo é aberto e depois de lido é fechado.
  with zipfile.ZipFile(arquivo, 'r') as zip_ref:
      zip_ref.extractall(diretorio_temp)
  print("ok")

def lerXML(arquivo: str = '\\dados\\xml_zip\\temp\\curriculo.xml', deleta: bool = True):
  """
  Lê o arquivo XML na pasta 

  Parameters
  ----------
  arquivo : str
      Caminho do arquivo curriculo.xml

  deleta : bool
      Deleta arquivo após leitura

  Returns
  -------
  DataFrame : pd.DataFrame
      DataFrame com tags
  """ 
  local = os.path.dirname(os.path.abspath(__file__))
  arquivo = local+arquivo
  tree = ET.parse(arquivo)
  root = tree.getroot()
  if deleta == True:
    os.remove(arquivo)
  return tree, root

def estruturaXML(arquivo: str = '\\dados\\xml_zip\\temp\\curriculo.xml'):
  """
  Imprime a estrutura do arquivo XML dos currículos Lattes

  Parameters
  ----------
  caminho : str
      Caminho do arquivo curriculo.xml

  Returns
  -------
  Print
  """ 
  #abreZip(caminho,arquivo, pasta)
 
  x = etree.parse(arquivo)                                                                                # Lê o arquivo XML
  xml = etree.tostring(x, pretty_print=True)                                                              # Ajeita o XML
  raiz = etree.fromstring(xml)                                                                            # Recebe raíz (root) do arquivo XML
  arvore = etree.ElementTree(raiz)                                                                        # Recebe a estruta em árvore (tree) do arquivo XML
  arvore_bonita = collections.OrderedDict()                                                               # Dicionário Ordenado do Collections em branco
  for tag in raiz.iter():
      caminho = re.sub('\[[0-9]+\]', '', arvore.getpath(tag))                                             # Substittui números por ''
      if caminho not in arvore_bonita:
          arvore_bonita[caminho] = []
      if len(tag.keys()) > 0:
          arvore_bonita[caminho].extend(atributo for atributo in tag.keys()                               # Adiciona abributos que não foram adicionados 
                                         if atributo not in arvore_bonita[caminho])             
  for caminho, atributos in arvore_bonita.items():
      indent = int(caminho.count('/') - 1)                                                                # Conta identações de acordo com '/'
      espaço='    ' * indent                                                         
      a = espaço +','
      print('{0}({1}) {2} : [{3}]'.format(espaço, indent, caminho.split('/')[-1], ', '.join(f'{atributo}' # Imprime os resultados
                                           for atributo in atributos) if len(atributos) > 0 else '-'))


def tagsAtributos(tag: str, root, subnivel=False) -> list:
  """
  Adiciona tag aos cabeçalhos de colunas de DataFrame definidos.
  Caso os cabeçalhos não sejam declarados, todos receberam a tag.

  Parameters
  ----------
  tag : str
      DataFrame

  root : root XML
      objeto root devolvido pela função lerXML()

  Returns
  -------
  Tags e Abributos : list
      Devolve duas listas com as Tags e Atributos
  """ 
  info = [elemento for elemento in root.iter(tag)]
  if subnivel == True:
    tags=[child.tag for child in info[0]]
    atributos=[child.attrib for child in info[0]]
  else:
    tags=[child.tag for child in info]
    atributos=[child.attrib for child in info]
  return tags, atributos


def AbributoXMLparaDf(tag:str, root, subnivel=False):
  """
  Converte os atributos das tags de entrada

  Parameters
  ----------

  tag : str
      Tag dos dados de interesse

  root : root XML
      Objeto devo

  Returns
  -------
  DataFrame : pd.DataFrame
      DataFrame com tags
  """ 
  tags, atributos = tagsAtributos(tag, root, subnivel)
  return pd.DataFrame(atributos)


def artigos(root):
  """
  Adiciona tag aos cabeçalhos de colunas de DataFrame definidos.
  Caso os cabeçalhos não sejam declarados, todos receberam a tag.

  Parameters
  ----------
  DataFrame : pd.DataFrame
      DataFrame

  tag : str
      objeto root devolvido pela função lerXML()

  colunas : list
      Colunas cujas cabeçalhos receberão tags
  Returns
  -------
  DataFrame : pd.DataFrame
      DataFrame com os dados da tag selecionada
  """ 
  basicos = AbributoXMLparaDf("DADOS-BASICOS-DO-ARTIGO",root)                             # Coleta os dados básicos dos artigos no arquivo XML
  detalhes = AbributoXMLparaDf("DETALHAMENTO-DO-ARTIGO",root)                             # Coleta os dados detalhados dos artigos no arquivo XML
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")                         # Concatena os dados em uma lista
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]                   # Coleta os dados gerais do pesquisador no arquivo XML
  nome_completo = dados_gerais['NOME-COMPLETO']                                           # Recebe o nome completo do pesquisador
  completo['autor_ifusp']=nome_completo                                                   # Adiciona o nome do pesquisador ao dataframe dos artigos
  return completo


      # As funções abaixo não foram utilizadas no trabalho, mas funcionam!
      # Serão usadas e aperfeiçoadas em trablho futuros
def orientacaoMestrado(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def orientacaoDoutorado(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def participacaoDoutorado(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-DOUTORADO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def participacaoMestrado(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-MESTRADO', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def participacaoQualificacao(root):
  basicos = AbributoXMLparaDf('DETALHAMENTO-DA-PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO', root)
  detalhes = AbributoXMLparaDf('DADOS-BASICOS-DA-PARTICIPACAO-EM-BANCA-DE-EXAME-QUALIFICACAO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def participacaoApresentacao(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DA-APRESENTACAO-DE-TRABALHO', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DA-APRESENTACAO-DE-TRABALHO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def participacaoBancaConcurso(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DA-BANCA-JULGADORA-PARA-CONCURSO-PUBLICO', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DA-BANCA-JULGADORA-PARA-CONCURSO-PUBLICO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def participacaoBancaLDocencia(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DA-BANCA-JULGADORA-PARA-LIVRE-DOCENCIA', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DA-BANCA-JULGADORA-PARA-LIVRE-DOCENCIA', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def participacaoBancaTitular(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DA-BANCA-JULGADORA-PARA-PROFESSOR-TITULAR', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DA-BANCA-JULGADORA-PARA-PROFESSOR-TITULAR', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def organizacaoEvento(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DA-ORGANIZACAO-DE-EVENTO', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DA-ORGANIZACAO-DE-EVENTO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def trabalhoPublicado(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DO-TRABALHO', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DO-TRABALHO', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def orientacaoOutras(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

def orientacaoOutras(root):
  basicos = AbributoXMLparaDf('DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS', root)
  detalhes = AbributoXMLparaDf('DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS', root)
  completo = pd.concat([basicos, detalhes], axis=1, join="inner")
  dados_gerais = [prod.attrib for prod in root.iter('DADOS-GERAIS')][0]
  nome_completo = dados_gerais['NOME-COMPLETO']
  completo['autor_ifusp']=nome_completo
  return completo

      # -------- Execução do programa -------- #
lista_xmls = listarArquivos()                                              # Lista os arquivos XML em um diretório
lista = []                                                                 # Lista vazia para armazenar caminho para arquivos
for xml in lista_xmls:                                                     # Itera sob lista de caminhos dos arquivos XML coletando dados dos currículos
  abreZip(xml)                                                             # Abre arquivo ZIP, cria uma pasta "temp" para armazenar o arquivo "curriculo.XML"
  tree, root = lerXML()                                                    # Lê o arquivo XML
  a = artigos(root)                                                        # Coleta os dados de artigos do curriculo
  lista.append(a)                                                          # Adicionar os dados a lista
df_artigos = pd.concat(lista).reset_index()                                # Concatena os dados de artigos da "lista" em DataFrame
local = os.path.dirname(os.path.abspath(__file__))                         # Caminho da pasta em que o arquivo PY está sendo executado
df_artigos.to_csv(local+'\dados\coletas\df_lattes.csv', index = False)     # Salva os dados dos arquivos XML em um dataframe
print("-- Fim do programa --")
