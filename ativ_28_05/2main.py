

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Function to load and clean data
st.cache_data
def load_data(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()  # Remove espaços extras nos nomes das colunas
    return df

# Load the data
df = load_data('Life_Expectancy_Data.csv')

# Streamlit App Title
st.title('Análise da Expectativa de Vida')

# Data Cleaning and Preprocessing Section
st.header('Pré-processamento de Dados')
st.write('Visualização inicial dos dados:')
st.dataframe(df.head())

st.write('### Informações sobre os dados:')

info_df = pd.DataFrame({
    'Coluna': df.columns,
    'Tipo de Dado': df.dtypes.astype(str),
    'Valores Não Nulos': df.notnull().sum(),
    'Valores Ausentes': df.isnull().sum()
})
info_df['% Valores Ausentes'] = (info_df['Valores Ausentes'] / len(df) * 100).round(2)

st.dataframe(info_df.style.format({'% Valores Ausentes': '{:.2f}%'}))


st.header('Análises e Respostas às Perguntas')

# 1. Correlação com expectativa de vida
st.subheader('1. Fatores de Previsão e Expectativa de Vida')

correlation_matrix = df.corr(numeric_only=True)['Life expectancy']
st.write('Correlação com a Expectativa de Vida:')
st.write(correlation_matrix.sort_values(ascending=False))

st.write('Exemplo de relação: Expectativa de Vida vs. Escolaridade')
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='Schooling', y='Life expectancy', ax=ax)
st.pyplot(fig)

# 2. Gastos com saúde
st.subheader('2. Gastos com Saúde e Expectativa de Vida em Países com Baixa Expectativa de Vida')
low_le_countries = df[df['Life expectancy'] < 65].copy()
st.write('Países com Expectativa de Vida < 65:')
st.dataframe(low_le_countries.head())

fig, ax = plt.subplots()
sns.scatterplot(data=low_le_countries, x='Total expenditure', y='Life expectancy', ax=ax)
st.pyplot(fig)

# 3. Mortalidade infantil e adulta
st.subheader('3. Taxas de Mortalidade: Infantil e Adulta')

fig, ax = plt.subplots()
sns.scatterplot(data=df, x='infant deaths', y='Life expectancy', ax=ax)
st.pyplot(fig)

fig, ax = plt.subplots()
sns.scatterplot(data=df, x='Adult Mortality', y='Life expectancy', ax=ax)
st.pyplot(fig)

# 4. Hábitos e estilo de vida
st.subheader('4. Correlação com Hábitos Alimentares, Estilo de Vida, Exercícios, Fumo, Álcool')
lifestyle_cols = ['BMI', 'Alcohol', 'thinness  1-19 years', 'thinness 5-9 years', 'Income composition of resources', 'Schooling']

missing_cols = [col for col in lifestyle_cols if col not in df.columns]
if missing_cols:
    st.warning(f"Colunas ausentes: {missing_cols}")
else:
    st.write('Correlação com variáveis de estilo de vida:')
    st.write(df[lifestyle_cols + ['Life expectancy']].corr()['Life expectancy'].drop('Life expectancy'))

# 5. Escolaridade
st.subheader('5. Impacto da Escolaridade na Expectativa de Vida')
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='Schooling', y='Life expectancy', ax=ax)
st.pyplot(fig)

# 6. Álcool
st.subheader('6. Relação com o Consumo de Álcool')
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='Alcohol', y='Life expectancy', ax=ax)
st.pyplot(fig)

# 7. População (densidade como proxy)
st.subheader('7. Países Densamente Povoados e Expectativa de Vida')
fig, ax = plt.subplots()
sns.scatterplot(data=df, x='Population', y='Life expectancy', ax=ax)
st.pyplot(fig)

# 8. Imunização
st.subheader('8. Impacto da Cobertura de Imunização')
immunization_cols = ['Polio', 'Diphtheria']
for col in immunization_cols:
    if col in df.columns:
        fig, ax = plt.subplots()
        sns.scatterplot(data=df, x=col, y='Life expectancy', ax=ax)
        st.pyplot(fig)
    else:
        st.warning(f"Coluna ausente: {col}")

# Conclusão
st.header('Conclusão')
st.write('Após todas essas análises, espero ter respondido aos vários "porquês" de diferentes calamidades e suas origens!')