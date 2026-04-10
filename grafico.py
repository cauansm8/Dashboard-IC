import numpy as np
from dash import dcc, html
import plotly.express as px
from plotly.subplots import make_subplots
from calculo import gerarDf

def update_output(contents, filename):

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
                        title="Gráfico de Violino | Arquivo: " + filename[0] + "<br>"
                        )



        # Gráfico de Dispersão
        fig2 = px.scatter(df[0], x="OrigemCOP_ML", y="OrigemCOP_AP",
                        labels={"OrigemCOP_ML": "COP_ML (cm)", "OrigemCOP_AP": "COP_AP (cm)"}, 
                        title="Gráfico de Dispersão | Arquivo: " + filename[0] + "<br>"
                        )
        

        # Mapa de Calor
        fig3 = px.density_heatmap(df[0], x="OrigemCOP_ML", y="OrigemCOP_AP",
                        labels={"OrigemCOP_ML": "COP_ML (cm)", "OrigemCOP_AP": "COP_AP (cm)"}, 
                        title="Mapa de Calor | Arquivo: " + filename[0] + "<br>"
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

        title = "Arquivos: "

        for i in range (0, len(df)):
            soma = i + 1
            title += str(soma) + "- " + filename[i] + " | "

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
        fig1_sp.update_layout(title_text = "Gráfico de Violino <br>" + title)
        
        for i in range(len(df)):
            fig1_sp.update_xaxes(
                title_text = "COP_ML (cm)",
                row = i + 1,
                col = 1
            )

        fig2_sp.update_layout(title_text = "Gráfico de Dispersão <br>" + title)
        fig3_sp.update_layout(title_text = "Mapa de Calor <br>" + title)
        
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