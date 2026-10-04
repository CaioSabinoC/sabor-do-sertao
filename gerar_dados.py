import numpy as np
import pandas as pd

# Semente fixa para reproduzir os mesmos dados
np.random.seed(42)

# Configurações
n = 2000

cidades = [
    "Recife",
    "Olinda",
    "Caruaru",
    "Petrolina",
    "Garanhuns"
]

categorias = [
    "Hambúrguer",
    "Pizza",
    "Sanduíche",
    "Porção",
    "Bebida"
]

produtos = [
    "X-Sertão",
    "X-Bacon",
    "Pizza de Calabresa",
    "Pizza de Frango",
    "Sanduíche Natural",
    "Batata Frita",
    "Coxinha",
    "Refrigerante",
    "Suco",
    "Água"
]

formas_pagamento = [
    "Pix",
    "Cartão de crédito",
    "Cartão de débito",
    "Dinheiro"
]

# Datas ao longo de um ano
datas = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    periods=n
)

df = pd.DataFrame({
    "data": datas,
    "cidade": np.random.choice(cidades, n),
    "categoria": np.random.choice(categorias, n),
    "produto": np.random.choice(produtos, n),
    "quantidade": np.random.randint(1, 6, n),
    "forma_pagamento": np.random.choice(formas_pagamento, n),
    "avaliacao": np.round(
        np.random.uniform(1, 5, n),
        1
    )
})

# Valores unitários aleatórios
precos = np.random.uniform(8, 60, n)

# Faturamento da venda
df["total"] = np.round(
    df["quantidade"] * precos,
    2
)

# Criar alguns valores ausentes na avaliação
indices = np.random.choice(
    df.index,
    size=100,
    replace=False
)

df.loc[indices, "avaliacao"] = np.nan

# Ordenar por data
df = df.sort_values("data").reset_index(drop=True)

# Salvar CSV
df.to_csv(
    "vendas.csv",
    index=False
)

print("Arquivo vendas.csv criado com sucesso!")
print(f"Quantidade de vendas: {len(df)}")
print("\nPrimeiras linhas:")
print(df.head())
