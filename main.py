import dash
from dash import dcc, html, Output, Input, State
import plotly.express as px
import pandas as pd
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

    print (tipo_do_conteudo)
    print (string_do_conteudo)

    # decodifica o conteudo do arquivo para bytes (binário)
    conteudo_decodificado = base64.b64decode(string_do_conteudo)

    print (conteudo_decodificado)

    try:
        # decodifica/interpreta o conteúdo como utf-8
        # io.StringIO -> simula um txt, ou seja, "passa" o contéudo (normalizado) para um txt
        # dai o txt pode ser lido normalmente
        df = pd.read_csv(io.StringIO(conteudo_decodificado.decode('utf-8')))
                                
        # cria a figura do gráfico -> modelagem -> !!!! AQUI SERÁ ALTERADO PARA GERAR:
        #               gráfico de dispersão, gráfico de linhas e mapas de calor.
        fig = px.bar(df, x=df.columns[0], y=df.columns[1])

        # retorna a figura para o site
        return dcc.Graph(figure=fig)

    except:
        
        # tratamento de erro
        return html.Div(f"Ocorreu um erro ao ler o arquivo!")



# inicia o servidor Dash
if __name__ == '__main__':
    app.run()
