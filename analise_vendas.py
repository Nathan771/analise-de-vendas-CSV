import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

#Configuração do dataset

#caminho

arquivo_csv = Path(__file__).parent / "vendas.aleatorias.csv"

#leitura do dataset

df = pd.read_csv(arquivo_csv, encoding = "utf-8-sig")

print(" Dataset carregado com sucesso!")
print(f"Total de registros: {len(df)}")
print("\nVisualização inicial: ")
print(df.head())

#Limpeza e tratamento de dados


#Converter datas

df["data"] = pd.to_datetime(df["data"], errors = "coerce")

#Remover linhas com datas inválidas

df = df.dropna(subset=["data"])

#Garantir tipos corretos

df["quantidade"] = df["quantidade"].astype(int)
df["preco_unitario"] = df["preco_unitario"].astype(float)

#Criar coluna de faturamento

df["faturamento"] = df["quantidade"] * df["preco_unitario"]

#Analise descritivas

print("\n Resumo estatístico:")
print(df.describe())

#Faturamento total

faturamento_total = df["faturamento"].sum()
print(f"\n Faturamento total: R$ {faturamento_total:,.2f}")

#Categoria

faturamento_cat = df.groupby("categoria")["faturamento"].sum().sort_values(ascending=False)
print("\nFaturamento por categoria:")
print(faturamento_cat)

#Produtos mais vendidos

produtos_mais_vendidos = df.groupby("produto")["quantidade"].sum().sort_values(ascending=False)
print("\nTop 5 produtos mais vendidos:")
print(produtos_mais_vendidos.head(5))





