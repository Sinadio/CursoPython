# 📊 Global Data Tracker da COVID-19
# Autor: Sinadio Mbuvane
# Data: 2025-08-15

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =======================
# 1️⃣ CARREGAR DADOS COM TRATAMENTO DE ERROS
# =======================
while True:
    try:
        caminho_csv = input("Digite o caminho do arquivo CSV da COVID-19: ").strip()
        df = pd.read_csv(caminho_csv)
        break
    except FileNotFoundError:
        print("❌ Arquivo não encontrado! Tente novamente.")
    except pd.errors.EmptyDataError:
        print("❌ O arquivo está vazio! Escolha outro.")
    except Exception as e:
        print(f"⚠ Ocorreu um erro: {e}")

print("\n✅ Dados carregados com sucesso!")
print(df.head())

# =======================
# 2️⃣ TRATAR COLUNAS AUSENTES
# =======================
colunas_criticas = ["date", "state", "new_confirmed", "new_deaths"]

for col in colunas_criticas:
    if col not in df.columns:
        print(f"⚠ Coluna '{col}' não encontrada! Criando com valor 0.")
        df[col] = 0

# Remover linhas com valores nulos nas colunas principais
df = df.dropna(subset=colunas_criticas)

# Garantir que a coluna de datas está no formato datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Ordenar dados por data
df = df.sort_values(by="date")

# =======================
# 3️⃣ FILTRAR POR PAÍS E INTERVALO DE DATAS
# =======================
paises_disponiveis = df["state"].unique()
print("\n🌍 Estados/Regiões disponíveis:")
print(", ".join(map(str, paises_disponiveis)))

estado_escolhido = input("\nDigite o estado/região que deseja analisar: ").strip()

while estado_escolhido not in paises_disponiveis:
    print("❌ Estado inválido. Tente novamente.")
    estado_escolhido = input("Digite o estado/região que deseja analisar: ").strip()

data_inicio = input("Digite a data inicial (YYYY-MM-DD): ")
data_fim = input("Digite a data final (YYYY-MM-DD): ")

df_filtrado = df[(df["state"] == estado_escolhido) &
                 (df["date"] >= data_inicio) &
                 (df["date"] <= data_fim)]

if df_filtrado.empty:
    print("⚠ Nenhum dado encontrado para esse intervalo. Usando todos os dados do estado.")
    df_filtrado = df[df["state"] == estado_escolhido]

# =======================
# 4️⃣ ANÁLISE EXPLORATÓRIA
# =======================
df_estado = df[df["place_type"] == "state"].groupby("state").max(numeric_only=True)
df_estado["taxa_mortalidade"] = (df_estado["last_available_deaths"] / df_estado["last_available_confirmed"]) * 100

# 📈 Tendência de casos e mortes no estado
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_filtrado, x="date", y="new_confirmed", label="Novos Casos")
sns.lineplot(data=df_filtrado, x="date", y="new_deaths", label="Novas Mortes")
plt.title(f"Tendência de Casos e Mortes - {estado_escolhido}")
plt.xlabel("Data")
plt.ylabel("Quantidade")
plt.legend()
plt.show()

# 📊 Top 10 estados com mais casos
top_estados = df[df["place_type"] == "state"].groupby("state")["last_available_confirmed"].max().sort_values(ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=top_estados.values, y=top_estados.index, palette="Reds_r")
plt.title("Top 10 Estados com Mais Casos Confirmados")
plt.xlabel("Casos Confirmados")
plt.ylabel("Estado")
plt.show()

# 📊 Taxa de mortalidade
plt.figure(figsize=(10, 6))
sns.barplot(x=df_estado["taxa_mortalidade"].sort_values(ascending=False),
            y=df_estado.index, palette="coolwarm")
plt.title("Taxa de Mortalidade por Estado (%)")
plt.xlabel("Taxa de Mortalidade (%)")
plt.ylabel("Estado")
plt.show()

# =======================
# 5️⃣ INSIGHTS
# =======================
print("\n📌 Insights do Dataset:")
print(f"- Estado com mais casos confirmados: {top_estados.index[0]} ({top_estados.values[0]})")
print(f"- Estado com maior taxa de mortalidade: {df_estado['taxa_mortalidade'].idxmax()} ({df_estado['taxa_mortalidade'].max():.2f}%)")
print(f"- Estado com menor taxa de mortalidade: {df_estado['taxa_mortalidade'].idxmin()} ({df_estado['taxa_mortalidade'].min():.2f}%)")
