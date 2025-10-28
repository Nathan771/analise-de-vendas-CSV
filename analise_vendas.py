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

#Remvoer linhas com datas inválidas

df = df.dropna(subset=["data"])

#Garantir tipos corretos

df["quantidade"] = df["quantidade"].astype(int)
df["preco_unitario"] = df["preco_unitario"].astype(float)





