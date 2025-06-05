import streamlit as st
import backend as bk
import matplotlib.pyplot as plt

st.set_page_config(page_title='Dashboard de Vendas', layout='wide')

# Carregar dados usando backend
df = bk.carregar_dados()

# Mostrar primeiras linhas da tabela para confirmar o carregamento
st.title("Dashboard de Vendas - Dados")
st.dataframe(df.head())

# Filtros básicos
data_ini = st.sidebar.date_input("Data inicial", df['data_venda'].min().date())
data_fim = st.sidebar.date_input("Data final", df['data_venda'].max().date())
forma_pagamento = st.sidebar.selectbox("Forma de Pagamento", ['Todos'] + sorted(df['forma_pagamento'].unique()))
clientes = ['Todos'] + sorted(df['cliente'].unique())
clientes_selecionados = st.sidebar.multiselect("Cliente(s)", clientes, default='Todos')

# Aplicar filtros
df_filtrado = bk.aplicar_filtros(df, data_ini, data_fim, forma_pagamento, clientes_selecionados)

# Indicadores
total_vendas, ticket_medio, quantidade_total = bk.calcular_indicadores(df_filtrado)

st.subheader("Filtro de Vendas")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Faturamento Total", f"R$ {total_vendas:,.2f}")
col2.metric("🧾 Ticket Médio", f"R$ {ticket_medio:,.2f}")
col3.metric("📦 Quantidade Vendida", int(quantidade_total))

col1, col2 = st.columns(2)

# Evolução mensal das vendas
evolucao = bk.grafico_evolucao(df_filtrado)
fig, ax = plt.subplots(figsize=(6,3))
ax.bar(evolucao['mes'], evolucao['valor_total'], color='#034159')
ax.set_xlabel('Mês')
ax.set_ylabel('Valor Total (R$)')
ax.set_title('Vendas por Mês')
plt.xticks(rotation=45) 
with col1:
    st.subheader("📅 Evolução Mensal das Vendas")
    st.pyplot(fig)

# Top produtos
top = bk.top_produtos(df_filtrado)

fig2, ax2 = plt.subplots(figsize=(6,3))
ax2.bar(top['produto'], top['quantidade'], color='#FF9933')
ax2.set_ylabel('Quantidade Vendida')
ax2.set_title('Top Produtos')
plt.xticks(rotation=25)
with col2:
    st.subheader("🍧 Top Produtos")
    st.pyplot(fig2)

# Lucro por categoria
st.subheader("📈 Evolução do Lucro por Categoria")

# Agrupa por mês e categoria
df_lucro_cat = df_filtrado.copy()
df_lucro_cat['ano_mes'] = df_lucro_cat['data_venda'].dt.to_period('M')
lucro_categoria_mes = df_lucro_cat.groupby(['ano_mes', 'categoria'])['valor_total'].sum().reset_index()

# Converte 'ano_mes' para string para melhor plotagem
lucro_categoria_mes['ano_mes'] = lucro_categoria_mes['ano_mes'].astype(str)

# Pivot para ter categorias nas colunas
pivot_lucro = lucro_categoria_mes.pivot(index='ano_mes', columns='categoria', values='valor_total').fillna(0)

fig, ax = plt.subplots(figsize=(8, 4))
pivot_lucro.plot(ax=ax, marker='o')
ax.set_title("Evolução do Lucro por Categoria")
ax.set_xlabel("Mês")
ax.set_ylabel("Lucro (R$)")
ax.legend(title='Categoria')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)