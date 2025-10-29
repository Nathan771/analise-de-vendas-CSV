import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

#leitura do dataset

df = pd.read_csv(arquivo_selecionado, encoding = "utf-8-sig")

print(" Dataset carregado com sucesso!")
print(f"Total de registros: {len(df)}")
print("\nVisualização inicial: ")
print(df.head())


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

#coluna de mês e faturamento mensal

df ["mes"] = df["data"].dt.to_period("M").astype(str)
faturamento_mensal = df.groupby("mes")["faturamento"].sum()

# Visualização dos Gráficos

sns.set(style = "whitegrid")
figs = []

#Gráfico 1: Faturamento por categoria

fig, ax1 = plt.subplots(figsize = (8, 5))
sns.barplot(x=faturamento_cat.index, y = faturamento_cat.values, palette="viridis")
ax1.set_title("Faturamento por categoria")
ax1.set_xlabel("Categoria")
ax1.set_ylabel("Faturamento (R$)")
figs.append(fig)

"""plt.figure(figsize=(8, 5))
sns.barplot(x=faturamento_cat.index, y=faturamento_cat.values, palette = "viridis")
plt.title("Faturamento por categoria")
plt.xlabel("Categoria")
plt.ylabel("Faturamento (R$)")
plt.tight_layout()
plt.show()
"""
#Gráfico 2: 5 Produtos mais vendidos

fig2, ax2 = plt.subplots(figsize=(8, 5))
sns.barplot(
    x=produtos_mais_vendidos.head(5).index,
    y=produtos_mais_vendidos.head(5).values,
    palette = "magma",
    ax = ax2
        
)

ax2.set_title("Top 5 produtos mais vendidos")
ax2.set_xlabel("Produto")
ax2.set_ylabel("Quantidade vendida")
figs.append(fig2)

"""plt.figure(figsize=(8, 5))
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
"""
#Gráfico 3: Faturamento mensal

fig3, ax3 = plt.subplots(figsize= (8, 5))
sns.lineplot(x=faturamento_mensal.index, y=faturamento_mensal.values, marker = "o", color = "blue", ax = ax3)
ax3.set_title("Faturamento mensal")
ax3.set_xlabel("Mês")
ax3.set_ylabel("Faturamento (R$)")

for label in ax3.get_xticklabels():
    label.set_rotation(45)
figs.append(fig3)

"""df["mes"] = df["data"].dt.to.period("M").astype(str)
faturamento_mensal = df.groupby("mes")["faturamento"].sum()

plt.figure(figsize = (8, 5))
sns.lineplot(x=faturamento_mensal.index, y=faturamento_mensal.values, marker = "o", color="blue")
plt.title("Faturamento mensal")
plt.xlabel("Mês")
plt.ylabel("Faturamento (R$)")
plt.xticks(rotation = 45)
plt.tight_layout()
plt.show()
"""
# interface interativa

root = tk.Tk()
root.title("Análise de Vendas")
root.geometry("1920x1080")

indice_atual = 0
canvas = None

def mostrar_grafico():
    global canvas
    if canvas:
        canvas.get_tk_widget().pack_forget()
    fig = figs[indice_atual]
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)

def proximo():
    global indice_atual
    indice_atual = (indice_atual + 1) % len(figs)
    mostrar_grafico()

def anterior():
    global indice_atual
    indice = (indice - 1) % len(figs)
    mostrar_grafico()

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

btn_ant = tk.Button(frame_botoes, text=" <- Anterior", width = 12, command=anterior)
btn_ant.pack(side = "left", padx=10)

btn_prox = tk.Button(frame_botoes, text="Proximo ->", width=12, command=proximo)
btn_prox.pack(side="left", padx=10)

mostrar_grafico()



#Exportação 

saida_excel = arquivo_selecionado.parent / "resumo_faturamento.xlsx"
faturamento_cat.to_excel(saida_excel)

print(f"\n Relatório salvo em: {saida_excel}")


#manter a janela aberta

root.mainloop()




