import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIGURACAO
# ==============================

st.set_page_config(
    page_title="Sabor do Sertao",
    page_icon="🌵",
    layout="wide"
)

# ==============================
# CARREGAR DADOS
# ==============================

df = pd.read_csv("vendas.csv")

df["data"] = pd.to_datetime(df["data"])

# ==============================
# TRATAMENTO DOS DADOS
# ==============================

df["avaliacao"] = df["avaliacao"].fillna(
    df["avaliacao"].median()
)

# ==============================
# FILTROS
# ==============================

st.sidebar.header("🔎 Filtros")

# Cidade
cidades = sorted(df["cidade"].unique())

cidades_selecionadas = st.sidebar.multiselect(
    "🏙️ Cidade",
    cidades,
    default=cidades
)

# Categoria
categorias = sorted(df["categoria"].unique())

categorias_selecionadas = st.sidebar.multiselect(
    "🍔 Categoria",
    categorias,
    default=categorias
)

# Data
data_min = df["data"].min().date()
data_max = df["data"].max().date()

periodo = st.sidebar.date_input(
    "📅 Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max
)

# ==============================
# APLICAR FILTROS
# ==============================

df_filtrado = df[
    (df["cidade"].isin(cidades_selecionadas))
    & (df["categoria"].isin(categorias_selecionadas))
].copy()

if len(periodo) == 2:

    data_inicio = pd.Timestamp(periodo[0])

    data_fim = (
        pd.Timestamp(periodo[1])
        + pd.Timedelta(days=1)
    )

    df_filtrado = df_filtrado[
        (df_filtrado["data"] >= data_inicio)
        & (df_filtrado["data"] < data_fim)
    ]

# ==============================
# TITULO
# ==============================

st.title(
    "🌵 Painel de Analise de Dados - Sabor do Sertao"
)

st.write(
    "Analise das vendas da rede de lanchonetes."
)

st.info(
    f"📊 {len(df_filtrado):,} vendas encontradas "
    "com os filtros selecionados."
)

# ==============================
# NIVEL 1 - EXPLORACAO
# ==============================

st.header("1. Exploracao dos Dados")

st.subheader("Primeiras linhas")

st.dataframe(
    df_filtrado.head()
)

st.subheader("Estatisticas descritivas")

st.dataframe(
    df_filtrado.describe()
)

st.subheader("Valores ausentes")

valores_ausentes = df_filtrado.isnull().sum()

st.dataframe(
    valores_ausentes.rename("Valores ausentes")
)

st.caption(
    "Os valores ausentes da coluna 'avaliacao' "
    "foram preenchidos utilizando a mediana, "
    "pois ela e menos sensivel a valores extremos."
)

# ==============================
# NIVEL 2 - KPIs
# ==============================

st.header("2. Indicadores de Desempenho")

if len(df_filtrado) > 0:

    faturamento_total = df_filtrado["total"].sum()

    numero_vendas = len(df_filtrado)

    ticket_medio = df_filtrado["total"].mean()

    avaliacao_media = df_filtrado["avaliacao"].mean()

else:

    faturamento_total = 0

    numero_vendas = 0

    ticket_medio = 0

    avaliacao_media = 0

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💰 Faturamento Total",
        f"R$ {faturamento_total:,.2f}"
    )

with col2:

    st.metric(
        "🧾 Numero de Vendas",
        f"{numero_vendas:,}"
    )

with col3:

    st.metric(
        "🎟️ Ticket Medio",
        f"R$ {ticket_medio:,.2f}"
    )

with col4:

    st.metric(
        "⭐ Avaliacao Media",
        f"{avaliacao_media:.2f}"
    )

# ==============================
# NIVEL 4 - GRAFICOS
# ==============================

st.header("3. Visualizacoes")

aba1, aba2, aba3, aba4 = st.tabs(
    [
        "📈 Faturamento Mensal",
        "🏙️ Faturamento por Cidade",
        "🏆 Top 5 Produtos",
        "💳 Formas de Pagamento"
    ]
)

# ==============================
# GRAFICO 1
# FATURAMENTO MENSAL
# ==============================

with aba1:

    mensal = (
        df_filtrado
        .groupby(
            df_filtrado["data"].dt.to_period("M")
        )["total"]
        .sum()
        .reset_index()
    )

    mensal["data"] = mensal["data"].astype(str)

    fig_mensal = px.line(
        mensal,
        x="data",
        y="total",
        markers=True,
        title="Faturamento Mensal"
    )

    fig_mensal.update_layout(
        xaxis_title="Mes",
        yaxis_title="Faturamento (R$)"
    )

    st.plotly_chart(
        fig_mensal,
        use_container_width=True
    )

# ==============================
# GRAFICO 2
# FATURAMENTO POR CIDADE
# ==============================

with aba2:

    cidade = (
        df_filtrado
        .groupby("cidade")["total"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_cidade = px.bar(
        cidade,
        x="cidade",
        y="total",
        title="Faturamento por Cidade",
        text_auto=".2f"
    )

    fig_cidade.update_layout(
        xaxis_title="Cidade",
        yaxis_title="Faturamento (R$)"
    )

    st.plotly_chart(
        fig_cidade,
        use_container_width=True
    )

# ==============================
# GRAFICO 3
# TOP 5 PRODUTOS
# ==============================

with aba3:

    produtos = (
        df_filtrado
        .groupby("produto")["quantidade"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    fig_produtos = px.bar(
        produtos,
        x="quantidade",
        y="produto",
        orientation="h",
        title="Top 5 Produtos por Quantidade Vendida",
        text_auto=True
    )

    fig_produtos.update_layout(
        xaxis_title="Quantidade Vendida",
        yaxis_title="Produto"
    )

    st.plotly_chart(
        fig_produtos,
        use_container_width=True
    )

# ==============================
# GRAFICO 4
# FORMAS DE PAGAMENTO
# ==============================

with aba4:

    pagamentos = (
        df_filtrado["forma_pagamento"]
        .value_counts()
        .reset_index()
    )

    pagamentos.columns = [
        "forma_pagamento",
        "quantidade"
    ]

    fig_pagamento = px.pie(
        pagamentos,
        names="forma_pagamento",
        values="quantidade",
        title="Distribuicao das Formas de Pagamento"
    )

    st.plotly_chart(
        fig_pagamento,
        use_container_width=True
    )

# ==============================
# NIVEL 5 - INSIGHTS
# ==============================

st.header("4. Insights Gerenciais")

if len(df_filtrado) > 0:

    # Cidade com maior faturamento
    faturamento_por_cidade = (
        df_filtrado
        .groupby("cidade")["total"]
        .sum()
        .sort_values(ascending=False)
    )

    cidade_destaque = faturamento_por_cidade.index[0]

    faturamento_cidade = faturamento_por_cidade.iloc[0]

    # Produto mais vendido
    quantidade_por_produto = (
        df_filtrado
        .groupby("produto")["quantidade"]
        .sum()
        .sort_values(ascending=False)
    )

    produto_destaque = quantidade_por_produto.index[0]

    quantidade_produto = quantidade_por_produto.iloc[0]

    # Forma de pagamento mais utilizada
    pagamentos_contagem = (
        df_filtrado["forma_pagamento"]
        .value_counts()
    )

    pagamento_destaque = pagamentos_contagem.index[0]

    quantidade_pagamento = pagamentos_contagem.iloc[0]

    st.markdown(
        f"""
### 💡 Insight 1 - Cidade

A cidade com maior faturamento e **{cidade_destaque}**,
com **R$ {faturamento_cidade:,.2f}** em vendas.

### 💡 Insight 2 - Produto

O produto mais vendido e **{produto_destaque}**,
com **{quantidade_produto} unidades vendidas**.

### 💡 Insight 3 - Pagamento

A forma de pagamento mais utilizada e
**{pagamento_destaque}**, com **{quantidade_pagamento} vendas**.
"""
    )

else:

    st.warning(
        "Nao existem dados para os filtros selecionados."
    )

# ==============================
# EXPORTACAO
# ==============================

st.subheader("📥 Exportar dados")

csv = df_filtrado.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Baixar dados filtrados",
    data=csv,
    file_name="vendas_filtradas.csv",
    mime="text/csv"
)
