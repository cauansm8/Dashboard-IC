import numpy as np
import base64
import io
import pandas as pd
from dash import html

# somente gera o df (é preciso separar para dps implementar a inserção de +1 arquivo)
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
