import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

#print("Fefe é muito bonita e tem um zoião, au au au au")

#Configuração do dataset


# Interface de seleção do arquivo

def selecionar_arquivos():
    root = tk.Tk()
    root.withdraw() #Oculta a janela principal
    caminho = filedialog.askopenfilename(
        title="Selecione o arquivo CSV de vendas",
        filetypes=[("Arquivos CSV", "*.csv")]
    )
    if not caminho:
        messagebox.showwarning("Aviso", "Nenhum arquivo foi selecionado. Encerrando o programa.")
        exit()
    return Path(caminho)

arquivo_selecionado = selecionar_arquivos()

"""
print(" Selecione um arquivo CSV: ")
arquivo_csv = selecionar_arquivos

if not arquivo_csv:
    arquivo_csv = arquivo_padrao
    print(f"Nenhum arquivo selecionado. Usando padrão: {arquivo_csv.name}")
else:
    arquivo_csv = Path(arquivo_csv)
    print(f"Arquivo selecionado: {os.path.basename(arquivo_csv)}")
"""
#leitura do dataset

df = pd.read_csv(arquivo_selecionado, encoding = "utf-8-sig")

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

# Visualização dos Gráficos

sns.set(style = "whitegrid")

#Gráfico 1: Faturamento por categoria

plt.figure(figsize=(8, 5))
sns.barplot(x=faturamento_cat.index, y=faturamento_cat.values, palette = "viridis")
plt.title("Faturamento por categoria")
plt.xlabel("Categoria")
plt.ylabel("Faturamento (R$)")
plt.tight_layout()
plt.show()

#Gráfico 2: 5 Produtos mais vendidos

plt.figure(figsize=(8, 5))
sns.barplot(
    x = produtos_mais_vendidos.head(5).index,
    y = produtos_mais_vendidos.head(5).values,
    palette = "magma"

)
plt.title("Top 5 produtos mais vendidos")
plt.xlabel("Produto")
plt.ylabel("Quantidade vendida")
plt.tight_layout()
plt.show()

#Gráfico 3: Faturamento mensal

df["mes"] = df["data"].dt.to.period("M").astype(str)
faturamento_mensal = df.groupby("mes")["faturamento"].sum()

plt.figure(figsize = (8, 5))
sns.lineplot(x=faturamento_mensal.index, y=faturamento_mensal.values, marker = "o", color="blue")
plt.title("Faturamento mensal")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.show()

#Exportação 

saida_excel = arquivo_selecionado.parent / "resumo_faturamento.xlsx"
faturamento_cat.to_excel(saida_excel)

print(f"\n Relatório salvo em: {saida_excel}")



