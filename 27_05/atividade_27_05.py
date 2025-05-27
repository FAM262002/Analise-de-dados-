import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

data_frame = pd.read_csv('clientes.csv', sep=',', encoding='latin1')

st.title("Análise de Cancelamento de Clientes de Cartão de Crédito")

# Upload do arquivo
arquivo = "clientes.csv"

if arquivo is not None:
    # Leitura do arquivo com codificação padrão em português
    df = pd.read_csv(arquivo, encoding="latin1")

    # Criar coluna binária para análise
    df["Cancelou"] = df["Categoria"].apply(lambda x: 1 if x == "Cancelado" else 0)

    st.subheader("Distribuição de Clientes")
    st.write(df["Categoria"].value_counts())

    # Comparações de médias
    colunas_analise = [
        "Meses como Cliente",
        "Taxa de Utilização Cartão",
        "Contatos 12m",
        "Valor Transacoes 12m",
        "Qtde Transacoes 12m"
    ]

    # Cálculo das médias
    medias = df.groupby("Cancelou")[colunas_analise].mean()

    st.subheader("Comparação de Médias entre Clientes Ativos e Cancelados")
    st.dataframe(medias)

    # Gráfico das médias
    st.subheader("Gráfico Comparativo")
    fig, ax = plt.subplots(figsize=(10, 5))
    medias.T.plot(kind="bar", ax=ax)
    plt.xticks(rotation=45)
    plt.legend(["Cliente Ativo", "Cancelado"], title="Situação")
    st.pyplot(fig)


 # 1.Gráfico de barras com a contagem de tipos de cartão
    st.subheader("Distribuição de Tipos de Cartão (Gráfico de Barras)")
    fig_pizza_corrigido, ax_pizza_corrigido = plt.subplots()
    df["Categoria Cartão"].value_counts().plot(kind='bar', ax=ax_pizza_corrigido, color='skyblue')
    ax_pizza_corrigido.set_ylabel("Número de Clientes")
    ax_pizza_corrigido.set_xlabel("Tipo de Cartão")
    st.pyplot(fig_pizza_corrigido)

    # 2. Gráfico de barras: Valor total de transações por tipo de cartão
    st.subheader("Valor Total de Transações por Tipo de Cartão")
    valor_trans_por_cartao = df.groupby("Categoria Cartão")["Valor Transacoes 12m"].sum().sort_values()
    fig3, ax3 = plt.subplots()
    sns.barplot(x=valor_trans_por_cartao.values, y=valor_trans_por_cartao.index, ax=ax3)
    ax3.set_xlabel("Valor Total de Transações (últimos 12 meses)")
    st.pyplot(fig3)



ax.set_title("Limite Disponível vs Inatividade")
ax.set_xlabel("Limite Disponível (R$)")
ax.set_ylabel("Meses Inativo")
ax.legend(title="Tipo de Cartão")


st.subheader("Possíveis Ações da Empresa")
st.markdown("""
    - Incentivar clientes com **baixa utilização** do cartão.
    - Reduzir inatividade com **promoções personalizadas**.
    - Acompanhar clientes que fazem **poucos contatos e transações**.
    - Criar estratégias para **reter clientes antigos**.
    - Clientes com **cartões mais simples (Blue)** concentram maior número de cancelamentos — avaliar upgrade ou benefícios.
    - **Menor valor de transações** pode indicar desinteresse → campanhas de incentivo ao uso.
    - Clientes com **menos dependentes** e **baixa interação** (poucos contatos) podem estar mais propensos a sair → investir em engajamento.
    - Criar material educativo sobre como usar melhor o cartão (limite, benefícios, segurança).
                    """)