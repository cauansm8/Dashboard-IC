import dash
from dash import dcc, html, Output, Input, State
import grafico



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
    State('upload-arquivo', 'filename')
)

def update_output(contents, filename):
    return grafico.update_output(contents, filename)

if __name__ == '__main__':
    app.run()