# - Título: 
#    Raspador WoS
# - Descrição:
#     O programa se identifica na plataforma Web of Science, executa buscas e exporta os resultados no formato Excel (disponibilizado pela própria WoS)
#     ATENÇÃO: programa foi executado em no segundo semestre de 2021. Mudanças no código das páginas da WoS provavelmente deixaram o programa inoperante. 
# - Autor:
#      Marlon Resende Faria
# - Orientador:
#       Alfredo Goldman vel Lejbman 


#-------- Bibliotecas --------#
from selenium import webdriver
import pandas as pd
import os
driver = webdriver.Chrome()                                                     # Seleciona o Browser que será usado. Firefox também pode ser usado.

local = os.path.dirname(os.path.abspath(__file__))

# importa a lista de IDs para realizar as buscas
df=pd.read_excel(local + "\dados\listaID.xlsx")
df1 = df[df['Identificador Web of Science']=='Não disponível']['Nome']          # Seleciona os nomes dos pesquisadores que não têm Research ID informado na lista
lista_nomes=df1['Nome']



#---------- Login ----------#
url=r'https://access.clarivate.com/login?app=wos&alternative=true&shibShireURL=https:%2F%2Fwww.webofknowledge.com%2F%3Fauth%3DShibboleth&shibReturnURL=https:%2F%2Fwww.webofknowledge.com%2F%3Fmode%3DNextgen%26action%3Dtransfer%26path%3D%252Fwos%252Fwoscc%252Fbasic-search%26DestApp%3DUA&referrer=mode%3DNextgen%26path%3D%252Fwos%252Fwoscc%252Fbasic-search%26DestApp%3DUA%26action%3Dtransfer&roaming=true'
driver.get(url)

username = 'sicrano@usp.br'                                                     # usuário no Web of Science
password = '1234567'                                                            # senha no Web of Science
nameidElem = driver.find_element_by_id('mat-input-0')                           # campo para usuário
nameidElem.send_keys(username)                                                  # entra com o username no campo
pwdidElem = driver.find_element_by_id('mat-input-1')                            # campo para senha
pwdidElem.send_keys(password)                                                   # entra com a senha no campo
continueElem = driver.find_element_by_id("signIn-btn")                          # botão de enviar
result = continueElem.submit()                                                  # envia os dados de login


#--------- Busca em loop ------------#
lista_erros=[]                                                                   # lista funciona como um log de erros, caso ocorram
for identificador in lista_nomes[100:]:                                          # itera sob a lista de IDs
    searchbox = driver.find_element_by_name("search-main-box")                   # elemento da página da caixa de busca
    searchbox.clear()                                                            # limpa a caixa de busca
    time.sleep(1)                                                                # aguarda um 1 segundo para carregamento

    searchbox.send_keys(identificador)                                           # insere o Reseacher ID do pesquisador
    time.sleep(3)                                                                # aguarda 3 segundos para entrada de dados
  
    button=driver.find_elements_by_xpath("//*[contains(text(), 'Pesquisar')]")   # identifica o botão "Pesquisar"
    button[2].click()                                                            # clica no botão pesquisar
    time.sleep(3)                                                                # aguarda 3 segundos para carregar o resultado da busca
    aviso=driver.find_elements_by_xpath("//*[contains(text(), 'Sua pesquisa não retornou nenhum resultado')]") # Busca pelo aviso de falha na busca: Resultado não encontrado

    if len(aviso)>0:                                                             # se aviso é uma lista não vazia
        lista_erros.append(identificador)                                        # adiciona o identificador do pesquisador cuja a pesquisa falhou
        driver.refresh()                                                         # recarrega a página
        continue                                                                 # pula o teste condicional e vai para o próximo item do laço

    else:
        # Identifica o botão de exportar os resultados de busca
        button = driver.find_elements_by_xpath("//button[@class='mat-focus-indicator mat-menu-trigger cdx-but-md cdx-but-white-background margin-right-10--reversible mat-button mat-stroked-button mat-button-base mat-primary']")
        button[0].click()
        time.sleep(1)
        button=driver.find_elements_by_xpath("//*[contains(text(), 'Excel')]")               # Encontra a opção Excel para formato dos dados que serão exportados
        button[1].click()
        time.sleep(1)
        button = driver.find_elements_by_xpath("//span[@class='dropdown-text']")             # Encontra as opções de completeza dos dados
        button[0].click()
        time.sleep(1)
        button=driver.find_elements_by_xpath("//*[contains(text(), 'Registro completo')]")   # seleciona registro completo (mais colunas de dados)
        button[0].click()
        time.sleep(1)
        button=driver.find_elements_by_xpath("//*[contains(text(), 'Exportar')]")            # finalmente exporta.
        button[1].click()
        time.sleep(10)                                                                       # aguarda um intervalo maior para que dê tempo do iniciar o download do XLS
        driver.back()                                                                        # Volta para página anterior

df = pd.DataFrame(lista_erros)
df.to_csv(local + 'data\logs\log_erros_raspador_wos.csv', index=False)
