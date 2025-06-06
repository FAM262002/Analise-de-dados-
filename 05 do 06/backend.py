import pandas as pd

df = pd.read_csv('dados_vendas_acai.csv', parse_dates=['data_venda'])
df_filtrado = df

def carregar_dados():
    df = pd.read_csv("dados_vendas_acai.csv", parse_dates=['data_venda'])
    return df

def top5_clientes_resumo(df):
    # 1. Top 5 clientes pelo valor total gasto
    total_gasto = df.groupby('cliente')['valor_total'].sum()
    top5_clientes = total_gasto.sort_values(ascending=False).head(5).index.tolist()
    
    df_top5 = df[df['cliente'].isin(top5_clientes)]
    
    # 2. Valor total gasto por cliente (para exibir)
    valor_gasto = df_top5.groupby('cliente')['valor_total'].sum()
    
    # 3. Forma de pagamento mais usada por cliente (contagem)
    forma_mais_usada = (
        df_top5.groupby(['cliente', 'forma_pagamento'])
        .size()
        .reset_index(name='contagem')
        .sort_values(['cliente', 'contagem'], ascending=[True, False])
        .drop_duplicates(subset=['cliente'], keep='first')
        .set_index('cliente')['forma_pagamento']
    )
    
    # 4. Produto mais consumido (quantidade) por cliente
    produto_mais_consumido = (
        df_top5.groupby(['cliente', 'produto'])['quantidade']
        .sum()
        .reset_index()
        .sort_values(['cliente', 'quantidade'], ascending=[True, False])
        .drop_duplicates(subset=['cliente'], keep='first')
        .set_index('cliente')['produto']
    )
    
    # Monta o dataframe final
    resumo = pd.DataFrame({
        'Valor Total Gasto': valor_gasto,
        'Forma de Pagamento Mais Usada': forma_mais_usada,
        'Produto Mais Consumido': produto_mais_consumido
    })
    
    # Opcional: ordena por valor gasto decrescente
    resumo = resumo.sort_values('Valor Total Gasto', ascending=False)
    
    return resumo

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