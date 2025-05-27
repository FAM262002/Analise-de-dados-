import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("dados_alunos_escola.csv")

df = pd.read_csv("dados_alunos_escola.csv", sep=',', encoding='utf-8')

linha = st.sidebar.selectbox("Escolha a qual das seguintes materias deseja consultar:", ['nota_portugues','nota_ciencias','nota_matematica'])
st.subheader(f"Geral", divider = True)
st.write(df[linha].describe())


st.subheader(f"Media de {linha}", divider=True)
st.write(df[linha].mean())


st.subheader(f"Mediana de {linha}", divider=True)
st.write(df[linha].median())


st.subheader(f"Moda de {linha}", divider=True)
st.write(df[linha].mode())


st.subheader(f"Variança de {linha}", divider=True)
st.write(df[linha].var())


st.subheader(f"Amplitude de {linha}", divider=True)
st.write(df[linha].max() - df[linha].min())


st.subheader(f"Frequencia de {linha}", divider=True)
st.write(df[linha].mean())


st.subheader("Alunos com Frequência Abaixo de 75%")
alunos_baixa_frequencia = df[df['frequencia_%'] < 75]
st.dataframe(alunos_baixa_frequencia)
if not alunos_baixa_frequencia.empty:
    st.write(f"Média geral das notas para estes alunos: {(alunos_baixa_frequencia[['nota_matematica', 'nota_portugues', 'nota_ciencias']].mean().mean()):.2f}")
else:
    st.write("Não há alunos com frequência abaixo de 75% neste conjunto de dados.")

st.subheader("Nota Média por Cidade e Matéria")
nota_media_cidade_materia = df.groupby('cidade')[[linha]].mean().round(2)
st.dataframe(nota_media_cidade_materia)

# --- Classificação de Notas ---
st.header("Classificação de Notas")

def classificar_nota(nota):
    if nota < 3.0:
        return 'Reprovado'
    elif nota < 6.0:
        return 'Exame'
    else:
        return 'Aprovado'

df['classificacao_matematica'] = df['nota_matematica'].apply(classificar_nota)
df['classificacao_portugues'] = df['nota_portugues'].apply(classificar_nota)
df['classificacao_ciencias'] = df['nota_ciencias'].apply(classificar_nota)

st.subheader("Contagem de Alunos por Classificação")
classificacao_counts = df[['classificacao_matematica', 'classificacao_portugues', 'classificacao_ciencias']].apply(pd.value_counts)
st.dataframe(classificacao_counts)

st.subheader("Contagem de Notas Específicas")
st.write(f"Quantidade de alunos com nota menor que 3.0 em Matemática: {len(df[df['nota_matematica'] < 3.0])}")
st.write(f"Quantidade de alunos com nota menor que 5.0 em Matemática: {len(df[df['nota_matematica'] < 5.0])}")
st.write(f"Quantidade de alunos com nota menor que 7.0 em Matemática: {len(df[df['nota_matematica'] < 7.0])}")
st.write(f"Quantidade de alunos com nota menor que 9.0 em Matemática: {len(df[df['nota_matematica'] < 9.0])}")
st.write(f"Quantidade de alunos com nota igual a 10.0 em Matemática: {len(df[df['nota_matematica'] == 10.0])}")

st.subheader("Cidades com Melhor e Pior Nota por Matéria")
for materia in ['nota_matematica', 'nota_portugues', 'nota_ciencias']:
    media_por_cidade = df.groupby('cidade')[materia].mean()
    if not media_por_cidade.empty:
        cidade_melhor = media_por_cidade.idxmax()
        cidade_pior = media_por_cidade.idxmin()
        st.write(f"**{materia.replace('nota_', '').capitalize()}:** Melhor - {cidade_melhor} ({media_por_cidade.max():.2f}), Pior - {cidade_pior} ({media_por_cidade.min():.2f})")
    else:
        st.write(f"Não há dados para calcular a melhor/pior cidade para {materia.replace('nota_', '').capitalize()}.")

plt.hist(df['nota_matematica'], bins=10)
plt.title("Distribuição de Notas de Matemática")
plt.xlabel("nota")
plt.ylabel("Frequência_%")
st.pyplot(plt)
plt.clf()  # limpa a figura

plt.hist(df['nota_ciencias'], bins=10)
plt.title("Distribuição de Notas de Ciências")
plt.xlabel("nota")
plt.ylabel("Frequência_%")
st.pyplot(plt)
plt.clf()

plt.hist(df['nota_portugues'], bins=10)
plt.title("Distribuição de Notas de Português")
plt.xlabel("nota")
plt.ylabel("Frequência_%")
st.pyplot(plt)
plt.clf()