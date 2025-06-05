import pandas as pd

def carregar_dados():
    df = pd.read_csv('dados_vendas_acai.csv', parse_dates=['data_venda'])
    return df

def aplicar_filtros(df, data_ini, data_fim, forma_pagamento, clientes):
    df_filtrado = df[
        (df['data_venda'] >= pd.to_datetime(data_ini)) &
        (df['data_venda'] <= pd.to_datetime(data_fim))
    ]
    if forma_pagamento != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['forma_pagamento'] == forma_pagamento]
    if clientes and 'Todos' not in clientes:
        df_filtrado = df_filtrado[df_filtrado['cliente'].isin(clientes)]
    return df_filtrado

def calcular_indicadores(df):
    total_vendas = df['valor_total'].sum()
    ticket_medio = df['valor_total'].mean() if not df.empty else 0
    quantidade_total = df['quantidade'].sum()
    return total_vendas, ticket_medio, quantidade_total

def grafico_evolucao(df):
    df = df.copy()
    df['ano_mes'] = df['data_venda'].dt.to_period('M')
    agrupado = df.groupby('ano_mes')['valor_total'].sum().reset_index()
    agrupado['mes'] = agrupado['ano_mes'].astype(str)
    return agrupado[['mes', 'valor_total']]

def top_produtos(df, top_n=5):
    top = df.groupby('produto')['quantidade'].sum().sort_values(ascending=False).head(top_n).reset_index()
    return top

def lucro_por_categoria(df):
    lucro = df.groupby('categoria')['valor_total'].sum().reset_index()
    return lucro