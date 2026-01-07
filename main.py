import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt 
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
            'width': '20%',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px auto'
        },
        
        # permite mais de um arquivo por vez -> o 'contents' é uma lista 
        multiple=True  
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
    
    df = []

    # le o arquivos e passa como ao df como lista (mesmo se for só um arquivo inserido)
    for i in range(len(contents)):
        df.append(gerarDf(contents[i]))

    # caso 1 -> 1 arquivo (segue o que já foi implementado anteriormente)
    if len(df) == 1:

        # Gráfico de Violino com Box-Plot
        fig1 = px.violin(df[0], x="OrigemCOP_ML",
                        box=True, points='all', hover_data=df[0].columns,
                        labels={"OrigemCOP_ML": "COP_ML (cm)"}, 
                        title="Gráfico de Violino"
                        )



        # Gráfico de Dispersão
        fig2 = px.scatter(df[0], x="OrigemCOP_ML", y="OrigemCOP_AP",
                        labels={"OrigemCOP_ML": "COP_ML (cm)", "OrigemCOP_AP": "COP_AP (cm)"}, 
                        title="Gráfico de Dispersão"
                        )
        

        # Mapa de Calor
        fig3 = px.density_heatmap(df[0], x="OrigemCOP_ML", y="OrigemCOP_AP",
                        labels={"OrigemCOP_ML": "COP_ML (cm)", "OrigemCOP_AP": "COP_AP (cm)"}, 
                        title="Mapa de Calor"
                        )

        # linha preta no centro
        fig1.update_xaxes(zeroline = True, zerolinewidth = 2, zerolinecolor='black')
        fig2.update_xaxes(zeroline = True, zerolinewidth=  2, zerolinecolor='black')
        fig2.update_yaxes(zeroline = True, zerolinewidth = 2, zerolinecolor='black')

        # retorna um div com os gráficos para o site
        return html.Div([
            dcc.Graph(figure=fig1),
            dcc.Graph(figure=fig2),
            dcc.Graph(figure=fig3)
        ])
    
    # caso 2: para mais de um gráf -> subplots
    else:

        # cada subplot tem x (sendo x o numero de arquivos inseridos) colunas
        fig1_sp = make_subplots(rows = len(df), cols = 1)
        fig2_sp = make_subplots(rows = len(df), cols = 1)
        fig3_sp = make_subplots(rows = len(df), cols = 1)

        # subplot 1
        for i in range(len(df)):
            
            # Gráfico de Violino com Box-Plot
            fig1 = px.violin(df[i], x="OrigemCOP_ML",
                        box=True, points='all', hover_data = df[i].columns)
            
            # add o subplot 
            for trace in fig1.data:
                fig1_sp.add_trace(trace, row = i + 1, col = 1)

        # subplot 2
        for i in range(len(df)):

            # Gráfico de Dispersão
            fig2 = px.scatter(df[i], x="OrigemCOP_ML", y="OrigemCOP_AP")
            
            # add o subplot
            for trace in fig2.data:
                fig2_sp.add_trace(trace, row = i + 1, col = 1)

        # subplot 3
        for i in range(len(df)):

            # Mapa de Calor
            fig3 = px.density_heatmap(df[i], x="OrigemCOP_ML", y="OrigemCOP_AP")
            
            # add subplot
            for trace in fig3.data:
                fig3_sp.add_trace(trace, row = i + 1, col = 1)

        
        # colocando labels e titulo
        fig1_sp.update_layout(title_text = "Gráfico de Violino")
        
        for i in range(len(df)):
            fig1_sp.update_xaxes(
                title_text = "COP_ML (cm)",
                row = i + 1,
                col = 1
            )

        fig2_sp.update_layout(title_text = "Gráfico de Dispersão")
        fig3_sp.update_layout(title_text = "Mapa de Calor")
        
        for i in range(len(df)):
            fig2_sp.update_xaxes(
                title_text = "COP_ML (cm)",
                row = i + 1,
                col = 1
            )
            fig2_sp.update_yaxes(
                title_text = "COP_AP (cm)",
                row = i + 1,
                col = 1
            )
            fig3_sp.update_xaxes(
                title_text = "COP_ML (cm)",
                row = i + 1,
                col = 1
            )
            fig3_sp.update_yaxes(
                title_text = "COP_AP (cm)",
                row = i + 1,
                col = 1
            )

        # linha preta indicando o centro
        fig1_sp.update_xaxes(zeroline=True, zerolinewidth = 2, zerolinecolor='black')        
        fig2_sp.update_xaxes(zeroline=True, zerolinewidth = 2, zerolinecolor='black')
        fig2_sp.update_yaxes(zeroline=True, zerolinewidth = 2, zerolinecolor='black')

        # melhorando a altura
        fig1_sp.update_layout(height = 800)
        fig2_sp.update_layout(height = 800)
        fig3_sp.update_layout(height = 800)


        return html.Div([
            dcc.Graph(figure=fig1_sp),
            dcc.Graph(figure=fig2_sp),
            dcc.Graph(figure=fig3_sp)
        ])


# somente gera o df (e preciso separar para dps implementar a inserção de +1 arquivo)
def gerarDf (contents):
    
    tipo_do_conteudo, string_do_conteudo = contents.split(',')

    # decodifica o conteudo do arquivo para bytes (binário)
    conteudo_decodificado = base64.b64decode(string_do_conteudo)

    try:
        # decodifica/interpreta o conteúdo como utf-8
        # io.StringIO -> simula um txt, ou seja, "passa" o contéudo (normalizado) para um txt
        # dai o txt pode ser lido normalmente   
        
        #                                            esse sep indica o formato que separa as informações -> , + espaco
        df = pd.read_csv(io.StringIO(conteudo_decodificado.decode('utf-8')), sep=r",\s*", engine="python", header=None, names=['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])

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

        return df

    except Exception as e:
        return html.Div(f"Ocorreu um erro ao ler o arquivo! {e}")


if __name__ == '__main__':
    app.run()

