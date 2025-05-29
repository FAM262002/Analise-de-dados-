import sqlite3 as sql
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta


conn = sql.connect("livros.db", check_same_thread=False)
cursor = conn.cursor()

#autores
cursor.execute('''
CREATE TABLE IF NOT EXISTS autores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
''')

#categorias
cursor.execute('''
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL
)
''')

#livros
cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor_id TEXT NOT NULL,
    categoria_id TEXT NOT NULL,
    ano TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    FOREIGN KEY(autor_id) REFERENCES autores(id),
    FOREIGN KEY(categoria_id) REFERENCES categorias(id)
)
''')

#emprestimo
cursor.execute('''
CREATE TABLE IF NOT EXISTS emprestimos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    livro_id INTEGER NOT NULL,
    data_emprestimo TEXT NOT NULL,
    devolvido BOOLEAN NOT NULL,
    FOREIGN KEY(livro_id) REFERENCES livros(id)
)
''')
conn.commit()

cursor.execute("SELECT COUNT(*) FROM autores")
if cursor.fetchone()[0] == 0:
    autores = [
        ('Machado de Assis',),
        ('Clarice Lispector',),
        ('J. K. Rowling',),
        ('George Orwell',),
        ('Isaac Asimov',),
        ('J. R. R. Tolkien',),
        ('Stephen King',),
        ('Gabriel García Márquez',),
        ('Jane Austen',)
    ]
    cursor.executemany("INSERT INTO autores (nome) VALUES (?)", autores)
    conn.commit()

cursor.execute("SELECT COUNT(*) FROM categorias")
if cursor.fetchone()[0] == 0:
    categorias_de_livros = [
        ("Clássicos",),
        ("Ficção Científica",),
        ("Fantasia",),
        ("Mistério e Suspense",),
        ("Romance",),
        ("Terror",),
        ("História",),
        ("Autoajuda e Desenvolvimento Pessoal",)
    ]
    cursor.executemany("INSERT INTO categorias (categoria) VALUES (?)", categorias_de_livros)
    conn.commit()


cursor.execute("SELECT COUNT(*) FROM livros")
if cursor.fetchone()[0] == 0:
    livros = [
        ('Dom Casmurro', 1, 1, '1899', 3),
        ('A Hora da Estrela', 2, 4, '1977', 2),
        ('Harry Potter e a Pedra Filosofal', 3, 3, '1997', 5),
        ('1984', 4, 4, '1949', 4),
        ('Fundação', 5, 3, '1951', 6),
        ('O Senhor dos Anéis', 6, 3, '1954', 7),
        ('It - A Coisa', 7, 4, '1986', 3),
        ('Cem Anos de Solidão', 8, 1, '1967', 2),
        ('Orgulho e Preconceito', 9, 1, '1813', 4),
        ('Ensaio Sobre a Cegueira', 1, 4, '1995', 3)
    ]
    cursor.executemany("INSERT INTO livros (titulo, autor_id, categoria_id, ano, quantidade) VALUES (?, ?, ?, ?, ?)", livros)
    conn.commit()



st.title("📚 Mini Sistema de Biblioteca")

st.subheader("📋 Tabela:")
df = pd.read_sql_query('''
    SELECT
        l.id,
        l.titulo,
        a.nome AS autor,
        c.categoria AS categoria,
        l.ano,
        l.quantidade
    FROM livros l
    JOIN autores a ON l.autor_id = a.id
    JOIN categorias c ON l.categoria_id = c.id
''',conn)
st.dataframe(df)

# Filtro por ano
st.subheader("🔍 Pesquise aqui:")
valor_min = st.slider("Preço mínimo", 1800, 2025)
df_filtro = pd.read_sql_query("SELECT * FROM livros WHERE ano > ?", conn, params=(valor_min,))
st.dataframe(df_filtro)

# Estatísticas
st.subheader("📈 Estatísticas Atualizadas")

# Total de exemplares cadastrados (somatório das quantidades)
qtd_total_exemplares = cursor.execute('SELECT SUM(quantidade) FROM livros').fetchone()[0] or 0

# Total de empréstimos ativos (não devolvidos)
qtd_emprestimos_ativos = cursor.execute('SELECT COUNT(*) FROM emprestimos WHERE devolvido = 0').fetchone()[0]

# Total de empréstimos devolvidos
qtd_emprestimos_devolvidos = cursor.execute('SELECT COUNT(*) FROM emprestimos WHERE devolvido = 1').fetchone()[0]

# Total de empréstimos feitos
qtd_total_emprestimos = qtd_emprestimos_ativos + qtd_emprestimos_devolvidos

# Livros disponíveis (apenas cálculo geral — estoque real)
qtd_livros_disponiveis = qtd_total_exemplares - qtd_emprestimos_ativos
if qtd_livros_disponiveis < 0:
    qtd_livros_disponiveis = 0

# Exibição
st.metric("📚 Total de Exemplares", qtd_total_exemplares)
st.metric("📤 Empréstimos Ativos", qtd_emprestimos_ativos)
st.metric("✅ Devolvidos", qtd_emprestimos_devolvidos)
st.metric("📦 Livros Disponíveis Agora", qtd_livros_disponiveis)

#st.subheader("📈 Estatísticas")
#qtd_livros = cursor.execute('SELECT SUM(quantidade) FROM livros').fetchone()[0]
#if qtd_livros is None:
    #qtd_livros = 0

#qtd_emprestimos = cursor.execute('SELECT COUNT(*) FROM emprestimos').fetchone()[0]
#qtd_devolvidos = cursor.execute('SELECT COUNT(*) FROM emprestimos WHERE devolvido = 1').fetchone()[0]

#st.metric("Total de Livros (exemplares)", qtd_livros)
#st.metric("Total de Empréstimos", qtd_emprestimos)
#st.metric("Total Devolvidos", qtd_devolvidos)

# Livros por categoria

st.subheader("🧾 Livros Emprestados:")
df_select = pd.read_sql_query('''
    SELECT l.titulo, e.data_emprestimo, e.devolvido
    FROM emprestimos e
    JOIN livros l ON e.livro_id = l.id
''', conn)
st.dataframe(df_select)

st.markdown("### 🔵 Encerrar Empréstimo e Calcular Multa")
# Buscar empréstimos em aberto (não devolvidos)
df_emprestimos_abertos = pd.read_sql_query('''
    SELECT e.id, l.titulo, e.data_emprestimo
    FROM emprestimos e
    JOIN livros l ON e.livro_id = l.id
    WHERE e.devolvido = 0
''', conn)

if not df_emprestimos_abertos.empty:
    selected_row = st.selectbox(
        "Selecione um empréstimo para encerrar:",
        df_emprestimos_abertos.itertuples(index=False),
        format_func=lambda row: f"{row.titulo} (em {row.data_emprestimo})"
    )

    if st.button("Encerrar Empréstimo"):
        data_emprestimo = datetime.strptime(selected_row.data_emprestimo, "%Y-%m-%d")
        data_hoje = datetime.today()
        prazo_limite = data_emprestimo + timedelta(days=7)
        dias_atraso = (data_hoje - prazo_limite).days

        multa = 0.0
        if dias_atraso > 0:
            multa = dias_atraso * 0.15

        cursor.execute('UPDATE emprestimos SET devolvido = 1 WHERE id = ?', (selected_row.id,))
        conn.commit()

        st.success("📚 Empréstimo encerrado com sucesso!")
        if multa > 0:
            st.error(f"⚠️ Atraso de {dias_atraso} dias. Multa: R$ {multa:.2f}")
        else:
            st.info("✅ Devolução dentro do prazo. Sem multa.")
else:
    st.info("Nenhum empréstimo em aberto.")


conn.commit()

df_disponibilidade = pd.read_sql_query('''
    SELECT 
        l.id,
        l.titulo,
        l.quantidade AS total_exemplares,
        COALESCE(e.emprestimos_ativos, 0) AS emprestimos_ativos,
        (l.quantidade - COALESCE(e.emprestimos_ativos, 0)) AS disponiveis
    FROM livros l
    LEFT JOIN (
        SELECT livro_id, COUNT(*) AS emprestimos_ativos
        FROM emprestimos
        WHERE devolvido = 0
        GROUP BY livro_id
    ) e ON l.id = e.livro_id
''', conn)

# Exiba no Streamlit
st.subheader("Quantidade Disponível")
st.dataframe(df_disponibilidade)



#st.subheader("📊 Livros por Categoria")
#categoria_count = query_df('''
#SELECT categorias.nome AS categoria, COUNT(*) AS quantidade
#FROM livros
#JOIN categorias ON livros.categoria_id = categorias.id
#GROUP BY categoria_id
#''')
#st.bar_chart(categoria_count.set_index('categoria'))

# Formulário: Novo Livro
st.subheader("📘 Adicionar novo livro")
with st.form("form_livro"):
    titulo = st.text_input("Título")
    autor_id = st.number_input("ID do Autor", min_value=1)
    categoria_id = st.number_input("ID da Categoria", min_value=1)
    ano = st.number_input("Ano", min_value=1800, max_value=2025)
    quantidade = st.number_input("Quantidade disponível", min_value=0)
    submitted = st.form_submit_button("Salvar")
    if submitted:
        cursor.execute('''
            INSERT INTO livros (titulo, autor_id, categoria_id, ano, quantidade)
            VALUES (?, ?, ?, ?, ?)
        ''', (titulo, autor_id, categoria_id, ano, quantidade))
        conn.commit()
        st.success("Livro adicionado!")
        st.rerun()

# Formulário: Novo Empréstimo
st.subheader("📤 Registrar novo empréstimo")
with st.form("form_emprestimo"):
    livro_id = st.number_input("ID do Livro", min_value=1)
    data = st.date_input("Data do Empréstimo")
    devolvido = st.checkbox("Já devolvido?")
    send = st.form_submit_button("Registrar")
    if send:
        cursor.execute('''
            INSERT INTO emprestimos (livro_id, data_emprestimo, devolvido)
            VALUES (?, ?, ?)
        ''', (livro_id, data.strftime("%Y-%m-%d"), devolvido))
        conn.commit()
        st.success("Empréstimo registrado!")
        st.rerun()

# Edição de livro
st.subheader("✏️ Editar Livro")
with st.form("edit_livro"):
    edit_id = st.number_input("ID do Livro para editar", min_value=1)
    novo_nome = st.text_input("Novo título")
    nova_qtd = st.number_input("Nova quantidade", min_value=0)
    salvar_edicao = st.form_submit_button("Salvar alterações")
    if salvar_edicao:
        cursor.execute('''
            UPDATE livros SET titulo = ?, quantidade_disponivel = ? WHERE id = ?
        ''', (novo_nome, nova_qtd, edit_id))
        conn.commit()
        st.success("Livro atualizado!")
        st.rerun()

# Deletar livro ou autor
st.subheader("❌ Deletar Livro ou Autor")
with st.form("delete"):
    tipo = st.selectbox("Tipo", ["Livro", "Autor"])
    delete_id = st.number_input("ID para deletar", min_value=1)
    deletar = st.form_submit_button("Deletar")
    if deletar:
        if tipo == "Livro":
            cursor.execute('DELETE FROM livros WHERE id = ?', (delete_id,))
        else:
            cursor.execute('DELETE FROM autores WHERE id = ?', (delete_id,))
        conn.commit()
        st.success(f"{tipo} deletado com sucesso!")
        st.rerun()

conn.close()