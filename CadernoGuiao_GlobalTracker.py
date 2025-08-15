# 📊 Global Data Tracker da COVID-19
# Autor: Sinadio Mbuvane
# Data: 14/08/2025

# =======================
# IMPORTS
# =======================
import os
import io
import sys
import json
import math
import urllib.request
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# (opcional, para mapa coroplético)
try:
    import plotly.express as px
    HAS_PLOTLY = True
except Exception:
    HAS_PLOTLY = False

plt.rcParams["figure.figsize"] = (11, 6)
plt.rcParams["axes.grid"] = True

# =======================
# 1️⃣ RECOLHA & CARREGAMENTO
# =======================
OWID_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
CSV_LOCAL = "owid-covid-data.csv"

def ensure_dataset(path_local=CSV_LOCAL, url=OWID_URL):
    """
    Garante que o CSV existe localmente. Se não existir, baixa via urllib.
    """
    try:
        if not os.path.exists(path_local):
            print(f"⚠️ '{path_local}' não encontrado. Baixando de OWID...")
            urllib.request.urlretrieve(url, path_local)
            print(f"✅ Baixado para: {path_local}")
        else:
            print(f"✅ Encontrado dataset local: {path_local}")
    except Exception as e:
        print(f"❌ Falha ao obter dataset: {e}")
        sys.exit(1)

def load_data(path_local=CSV_LOCAL):
    try:
        df = pd.read_csv(path_local, low_memory=False)
        # Normalizar nomes (garantir minúsculas e underscores para consultas)
        df.columns = [c.strip() for c in df.columns]
        return df
    except pd.errors.EmptyDataError:
        print("⚠️ Arquivo CSV vazio.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {path_local}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado ao ler CSV: {e}")
        sys.exit(1)

ensure_dataset()
df = load_data()

print("📄 Amostra (5 linhas):")
print(df.head(5))
print("\n📂 Info:")
_ = df.info()

print("\n🔎 Nulos (top 20 colunas):")
print(df.isnull().sum().sort_values(ascending=False).head(20))

# =======================
# 2️⃣ LIMPEZA
# =======================
# datas
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])
df = df.sort_values("date")

# algumas colunas úteis (só cria se não existirem)
NUM_COLS_SUG = [
    "new_cases", "new_deaths", "total_cases", "total_deaths",
    "total_vaccinations", "people_vaccinated", "people_fully_vaccinated",
    "new_cases_smoothed", "new_deaths_smoothed",
    "hosp_patients", "icu_patients",
    "total_cases_per_million", "total_deaths_per_million",
    "people_fully_vaccinated_per_hundred"
]
for c in NUM_COLS_SUG:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

# manter apenas linhas de países (excluir regiões agregadas tipo continents e income groups)
# OWID marca países com 'iso_code' de 3 letras; agregados costumam começar com 'OWID_'
if "iso_code" in df.columns:
    df = df[~df["iso_code"].astype(str).str.startswith("OWID_")]

# =======================
# 3️⃣ ENTRADA DO UTILIZADOR (PAÍSES E DATAS)
# =======================
def ask_list(prompt, default_list):
    try:
        raw = input(f"{prompt} (separe por vírgula) [Enter para padrão {default_list}]: ").strip()
    except EOFError:
        raw = ""
    if not raw:
        return default_list
    return [x.strip() for x in raw.split(",") if x.strip()]

def ask_date(prompt, default_value):
    try:
        raw = input(f"{prompt} [Enter para {default_value}]: ").strip()
    except EOFError:
        raw = ""
    if not raw:
        return pd.to_datetime(default_value)
    return pd.to_datetime(raw, errors="coerce")

paises_default = ["Mozambique", "Brazil", "India", "United States", "Kenya"]
paises = ask_list("⭐ País(es) para analisar", paises_default)

date_min = pd.to_datetime("2020-01-01")
date_max = pd.to_datetime(df["date"].max()) if "date" in df.columns else pd.to_datetime("today")

dt_ini = ask_date("⭐ Data inicial (YYYY-MM-DD)", date_min.date().isoformat())
dt_fim = ask_date("⭐ Data final (YYYY-MM-DD)", date_max.date().isoformat())

if pd.isna(dt_ini): dt_ini = date_min
if pd.isna(dt_fim): dt_fim = date_max
if dt_ini > dt_fim:
    dt_ini, dt_fim = dt_fim, dt_ini  # inverte se o usuário errar

# filtro
mask = df["location"].isin(paises) & df["date"].between(dt_ini, dt_fim)
dff = df.loc[mask].copy()
if dff.empty:
    print("⚠️ Filtro resultou em DataFrame vazio. Ajuste países ou datas.")
    # para prosseguir com algo:
    dff = df[df["location"].isin(paises_default) & df["date"].between(date_min, date_max)].copy()

print(f"\n📌 Intervalo aplicado: {dt_ini.date()} → {dt_fim.date()}")
print(f"🌎 Países: {sorted(dff['location'].unique().tolist())}")

# =======================
# 4️⃣ EDA — LINHAS (CASOS/MORTES)
# =======================
def plot_lines(metric, title):
    if metric not in dff.columns:
        print(f"⚠️ Métrica '{metric}' não encontrada no dataset.")
        return
    plt.figure()
    for country in sorted(dff["location"].unique()):
        sub = dff[dff["location"] == country]
        plt.plot(sub["date"], sub[metric], label=country)
    plt.title(title)
    plt.xlabel("Data")
    plt.ylabel(metric.replace("_", " ").title())
    plt.legend()
    plt.tight_layout()
    plt.show()

plot_lines("new_cases", "Novos casos diários")
plot_lines("new_deaths", "Novas mortes diárias")
plot_lines("total_vaccinations", "Vacinações totais (cumulativas)")

# Versões suavizadas, se existirem
plot_lines("new_cases_smoothed", "Novos casos (suavizado)")
plot_lines("new_deaths_smoothed", "Novas mortes (suavizado)")

# =======================
# 5️⃣ BARRAS — TOP POR TOTAL DE CASOS/MORTES
# =======================
def last_known(df_countries, colname):
    if colname not in df_countries.columns:
        return pd.Series(dtype=float)
    # pega o último valor conhecido por país no período filtrado
    s = (df_countries
         .sort_values("date")
         .groupby("location")[colname]
         .last())
    return s.dropna().sort_values(ascending=False)

top_cases = last_known(dff, "total_cases").head(10)
top_deaths = last_known(dff, "total_deaths").head(10)

if not top_cases.empty:
    sns.barplot(x=top_cases.values, y=top_cases.index)
    plt.title("Top 10 países — Total de casos (último valor no período)")
    plt.xlabel("Total de casos")
    plt.ylabel("País")
    plt.tight_layout()
    plt.show()

if not top_deaths.empty:
    sns.barplot(x=top_deaths.values, y=top_deaths.index)
    plt.title("Top 10 países — Total de mortes (último valor no período)")
    plt.xlabel("Total de mortes")
    plt.ylabel("País")
    plt.tight_layout()
    plt.show()

# =======================
# 6️⃣ MAPA DE CALOR (CORRELAÇÃO)
# =======================
corr_cols = [c for c in [
    "new_cases","new_deaths","total_cases","total_deaths",
    "total_vaccinations","people_fully_vaccinated",
    "hosp_patients","icu_patients"
] if c in dff.columns]

if len(corr_cols) >= 2:
    corr = dff[corr_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
    plt.title("Mapa de calor — correlação entre métricas")
    plt.tight_layout()
    plt.show()
else:
    print("ℹ️ Colunas insuficientes para mapa de calor de correlação.")

# =======================
# 7️⃣ HOSPITALIZAÇÃO / UCI (se disponível)
# =======================
plot_lines("hosp_patients", "Pacientes hospitalizados")
plot_lines("icu_patients", "Pacientes em UCI")

# =======================
# 8️⃣ MAPA COROPLÉTICO (opcional)
# =======================
if HAS_PLOTLY and {"iso_code","location","date"}.issubset(dff.columns):
    # pega o último snapshot por país dentro do período
    snap = (dff
            .sort_values("date")
            .groupby(["iso_code","location"], as_index=False)
            .last())

    metric_choro = None
    for m in ["people_fully_vaccinated_per_hundred",
              "total_cases_per_million",
              "total_deaths_per_million",
              "total_cases"]:
        if m in snap.columns:
            metric_choro = m
            break

    if metric_choro:
        fig = px.choropleth(
            snap,
            locations="iso_code",
            color=metric_choro,
            hover_name="location",
            projection="natural earth",
            title=f"Mapa coroplético — {metric_choro.replace('_',' ').title()} (último valor no período)"
        )
        fig.show()
    else:
        print("ℹ️ Nenhuma métrica apropriada para coroplético encontrada.")
else:
    print("ℹ️ Plotly indisponível ou colunas necessárias ausentes; pulando coroplético.")

# =======================
# 9️⃣ INSIGHTS AUTOMÁTICOS
# =======================
def safe_name(x):
    return str(x) if not (isinstance(x, float) and math.isnan(x)) else "N/D"

insights = []

# Maior total de casos no final do período
if not top_cases.empty:
    insights.append(f"• Maior total de casos: {top_cases.index[0]} ({int(top_cases.iloc[0]):,})")

# Maior total de mortes no final do período
if not top_deaths.empty:
    insights.append(f"• Maior total de mortes: {top_deaths.index[0]} ({int(top_deaths.iloc[0]):,})")

# Melhor cobertura vacinal (se existir)
if "people_fully_vaccinated_per_hundred" in dff.columns:
    top_full = last_known(dff, "people_fully_vaccinated_per_hundred")
    if not top_full.empty:
        insights.append(f"• Maior cobertura de totalmente vacinados: {top_full.index[0]} ({top_full.iloc[0]:.1f}%)")

# Tendência recente (7 dias) de casos em cada país
for country in sorted(dff["location"].unique()):
    sub = dff[dff["location"] == country].set_index("date").sort_index()
    if "new_cases" in sub.columns and len(sub) >= 14:
        recent = sub["new_cases"].tail(14).rolling(7).mean()
        if recent.notna().sum() >= 2:
            trend = "alta" if recent.iloc[-1] > recent.iloc[-2] else "queda/estável"
            insights.append(f"• {country}: média móvel de novos casos em {trend} na última semana.")

print("\n📌 INSIGHTS:")
for line in insights:
    print(line)

print("\n✅ FIM — relatório gerado.")
