import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd
import numpy as np
import io
import base64

app = dash.Dash(__name__)


# estrutura do html
app.layout = html.Div([   
    
    # parágrafo inicial
    html.H1(("Visualização Interativa de Dados Coletados por Plataformas de Força"),
        style={"textAlign": "center"}), 
    
    # upload de arquivo
    dcc.Upload(     
        id='upload-arquivo',
        children=html.Div([
            html.A('Selecione um arquivo CSV')
        ]),
        style={
            'width': '50%',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px auto'
        },
        
        # permite somente um arquivo por vez
        multiple=False  
    ),
    
    # div para o gráfico -> quando o arquivo for inserido, ele automaticamente será lido e tentará gerar o gráfico
    html.Div(id='output-grafico')
])


# faz as chamadas (quando ocorre alguma mudança - evento)

@app.callback(
    
    # quando ocorrer algum evento, vai alterar a div com id output-grafico
    # o "children" é o gráfico que será passado a div
    Output('output-grafico', 'children'),

    # o callback é chamado quando ocorrer mudança no contents (conteúdo) do upload com id upload-arquivo
    Input('upload-arquivo', 'contents'),

)

def update_output(contents):

    # basicamente divide o conteudo (data:text/csv;base64,QUxVTSxCTg...) na vírgula
    # tipo_do_conteudo recebe -> data:text/csv;base64
    # string_do_conteudo recebe o conteúdo do arquivo (vai se transformar no nosso dataframe do gráfico)     
    tipo_do_conteudo, string_do_conteudo = contents.split(',')

    print (f"\n\nTipo do conteudo: {tipo_do_conteudo}")
    print (f"String do conteudo: {string_do_conteudo}\n\n")

    # decodifica o conteudo do arquivo para bytes (binário)
    conteudo_decodificado = base64.b64decode(string_do_conteudo)

    try:
        # decodifica/interpreta o conteúdo como utf-8
        # io.StringIO -> simula um txt, ou seja, "passa" o contéudo (normalizado) para um txt
        # dai o txt pode ser lido normalmente   
        
        #                                            esse sep indica o formato que separa as informações -> , + espaco
        df = pd.read_csv(io.StringIO(conteudo_decodificado.decode('utf-8')), sep=r",\s*", engine="python", header=None, names=['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])

        print (df.head())

        # az0 (espessura): medida de az0 transformada em metros, pois a plataforma de força está em metros
        az0 = 0.0433

        # Frequência de aquisição de dados da plataforma de força, em Hz
        freq_pf = 100

        # Calculando o COP (IMPORTANTE - alterei o cálculo para fazer tudo direto - sem o for - )
        #               com o for (de antes), o conteúdo estava sendo reescrito 
        cop_x = ((df['Fx'] * az0 - df['My']) / df['Fz']) * 100
        cop_y = ((df['Fy'] * az0 + df['Mx']) / df['Fz']) * 100
        x_tempo = np.arange(len(df)) / freq_pf

        # Jogando as informações ao df (adiciona nova coluna ao dataframe)
        df['COP_ML'] = cop_x
        df['COP_AP'] = cop_y
        df['Tempo'] = x_tempo


        # Ajustando para a origem (ponto inicial vira 0,0) - Tales usou isto para iniciar as coordenadas no centro (0,0)
        df['OrigemCOP_ML'] = df['COP_ML'] - df['COP_ML'][0]
        df['OrigemCOP_AP'] = df['COP_AP'] - df['COP_AP'][0]

        # Limites de cada eixo
        max_OrigemML = np.max(np.abs(df['OrigemCOP_ML']))
        max_OrigemAP = np.max(np.abs(df['OrigemCOP_AP']))
        origemlimite_extremo = np.max([max_OrigemML, max_OrigemAP]) # Tales usou esta variável para definir os limites do gráfico!

        # Comparando o head do df atual com o df anterior
        print (df.head())

        print ("\n\n\n(DEBUG) - CHEGOU AQUI?????")

        # cria a figura do gráfico -> modelagem -> !!!! AQUI SERÁ ALTERADO PARA GERAR:
        #               gráfico de dispersão, gráfico de linhas e mapas de calor.
        fig = px.line(df, x='OrigemCOP_ML', y='OrigemCOP_AP', markers=True)

        # retorna a figura para o site
        return dcc.Graph(figure=fig)

    except Exception as e:
        
        # tratamento de erro
        return html.Div(f"Ocorreu um erro ao ler o arquivo! {e}")



# inicia o servidor Dash
if __name__ == '__main__':
    app.run()
