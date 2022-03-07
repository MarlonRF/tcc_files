#--------------------------------------------------------------------------------#
#---------------------------------| BIBLIOTECAS |--------------------------------#
#--------------------------------------------------------------------------------#

import numpy as np
import pandas as pd
import numpy as np
import os
import dash

from dash import html, dcc, dash_table 
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


app = dash.Dash(__name__,
                title="TCC - BMAC"
                )
app._favicon = "favico.ico"

#-------------------------------------------------------------------------------#
#---------------------------------| FUNÇÔES |-------------------------#
#-------------------------------------------------------------------------------#
#here = os.path.dirname(os.path.abspath(__file__))
here ='C:\\Users\\Redone\\OneDrive\\Área de Trabalho\\IME-BMAC\\Trabalho de Conclusão\\Dash deploy Google Run (teste)'
#df=  pd.read_csv(here + '\\df_metricas.csv', 
                #encoding = 'utf8', 
                #encoding = "ISO-8859-1",
                #sep=';'
 #                )
df = pd.read_excel(here +'\\df_metricas.xlsx')
print(df)