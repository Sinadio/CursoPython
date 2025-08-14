# 📊 Global Data Tracker da COVID-19
# Autor: Sinadio Mbuvane
# Data: 14/08/2025

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# =======================
# 1️⃣ CARREGAR DADOS COM EXCEÇÕES
# =======================
caminho_csv = "caso_full.csv"

try:
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_csv):
        raise FileNotFoundError(f"⚠ Arquivo não encontrado: {caminho_csv}")

    df = pd.read_csv(caminho_csv)
    print("✅ Arquivo carregado com sucesso!\n")

except FileNotFoundError as e:
    print(e)
    exit()
except pd.errors.EmptyDataError:
    print("⚠ O arquivo CSV está vazio.")
    exit()
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
    exit()

# =======================
# 2️⃣ EXPLORAR DADOS COM REPETIÇÃO
# =======================
print("\n📂 Informações do dataset:")
print(df.info())

print("\n📋 Nome das colunas:")
for coluna in df.columns:
    print(f"- {coluna}")

print("\n🔍 Valores nulos por coluna:")
for coluna in df.columns:
    nulos = df[coluna].isnull().sum()
    print(f"{coluna}: {nulos} valores nulos")

# =======================
# 3️⃣ LIMPEZA DE DADOS
# =======================
colunas_criticas = ["date", "state", "new_confirmed", "new_deaths"]

# Garante que todas as colunas críticas existem antes de remover nulos
for coluna in colunas_criticas:
    if coluna not in df.columns:
        print(f"⚠ Coluna ausente no dataset: {coluna}")
        df[coluna] = None  # cria a coluna vazia para evitar erro

df = df.dropna(subset=colunas_criticas)

# Converter datas
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])  # remove datas inválidas

# Ordenar
df = df.sort_values(by="date")

# =======================
# 4️⃣ ANÁLISE EXPLORATÓRIA
# =======================
try:
    df_brasil = df[df["place_type"] == "state"].groupby("date").sum(numeric_only=True)
    df_brasil = df_brasil[["new_confirmed", "new_deaths"]]

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_brasil["new_confirmed"], label="Novos Casos")
    sns.lineplot(data=df_brasil["new_deaths"], label="Novas Mortes")
    plt.title("Tendência de Novos Casos e Mortes no Brasil")
    plt.xlabel("Data")
    plt.ylabel("Quantidade")
    plt.legend()
    plt.show()

except KeyError as e:
    print(f"⚠ Coluna ausente para gráfico: {e}")

# =======================
# 5️⃣ TOP 10 ESTADOS COM MAIS CASOS
# =======================
try:
    top_estados = (
        df[df["place_type"] == "state"]
        .groupby("state")["last_available_confirmed"]
        .max()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_estados.values, y=top_estados.index, palette="Reds_r")
    plt.title("Top 10 Estados com Mais Casos Confirmados")
    plt.xlabel("Casos Confirmados")
    plt.ylabel("Estado")
    plt.show()

except KeyError:
    print("⚠ Não foi possível calcular o Top 10 por falta de colunas necessárias.")

# =======================
# 6️⃣ TAXA DE MORTALIDADE POR ESTADO
# =======================
try:
    df_estado = df[df["place_type"] == "state"].groupby("state").max(numeric_only=True)
    df_estado["taxa_mortalidade"] = (
        df_estado["last_available_deaths"] / df_estado["last_available_confirmed"]
    ) * 100

    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=df_estado["taxa_mortalidade"].sort_values(ascending=False),
        y=df_estado.index,
        palette="coolwarm"
    )
    plt.title("Taxa de Mortalidade por Estado (%)")
    plt.xlabel("Taxa de Mortalidade (%)")
    plt.ylabel("Estado")
    plt.show()

except ZeroDivisionError:
    print("⚠ Erro: divisão por zero ao calcular taxa de mortalidade.")
except KeyError as e:
    print(f"⚠ Coluna ausente para cálculo de mortalidade: {e}")

# =======================
# 7️⃣ INSIGHTS
# =======================
try:
    print("\n📌 Insights do Dataset:")
    print(f"- Estado com mais casos confirmados: {top_estados.index[0]} ({top_estados.values[0]} casos)")
    print(
        f"- Estado com maior taxa de mortalidade: {df_estado['taxa_mortalidade'].idxmax()} ({df_estado['taxa_mortalidade'].max():.2f}%)")
    print(
        f"- Estado com menor taxa de mortalidade: {df_estado['taxa_mortalidade'].idxmin()} ({df_estado['taxa_mortalidade'].min():.2f}%)")

except Exception as e:
    print(f"⚠ Não foi possível gerar insights: {e}")
