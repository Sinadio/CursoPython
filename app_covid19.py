import os
import urllib.request
import pandas as pd
import streamlit as st

# URLs e ficheiro local
OWID_URL = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
CSV_LOCAL = "owid-covid-data.csv"


# Função para baixar dados com tratamento de exceção
def baixar_dados():
    try:
        st.info("📥 A baixar dados mais recentes da COVID-19...")
        urllib.request.urlretrieve(OWID_URL, CSV_LOCAL)
        st.success("✅ Download concluído com sucesso!")
    except Exception as e:
        st.error(f"❌ Erro ao baixar dados: {e}")
        if os.path.exists(CSV_LOCAL):
            st.warning("⚠️ Usando ficheiro local antigo.")
        else:
            st.stop()


# Função para carregar dados
@st.cache_data
def carregar_dados():
    # Baixar apenas se não existir
    if not os.path.exists(CSV_LOCAL):
        baixar_dados()

    # Tentar carregar ficheiro local
    try:
        df = pd.read_csv(CSV_LOCAL, low_memory=False)
    except Exception as e:
        st.error(f"Erro ao carregar ficheiro CSV: {e}")
        st.stop()

    # Limpeza de dados
    try:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

        if "iso_code" in df.columns:
            df = df[~df["iso_code"].astype(str).str.startswith("OWID_")]

        # Conversão numérica segura
        num_cols = [
            "new_cases", "new_deaths", "total_cases", "total_deaths",
            "total_vaccinations", "people_vaccinated", "people_fully_vaccinated",
            "new_cases_smoothed", "new_deaths_smoothed",
            "hosp_patients", "icu_patients",
            "total_cases_per_million", "total_deaths_per_million",
            "people_fully_vaccinated_per_hundred"
        ]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
    except Exception as e:
        st.error(f"Erro ao limpar dados: {e}")
        st.stop()

    return df


# APP STREAMLIT
st.set_page_config(page_title="Painel COVID-19", layout="wide")
st.title("📊 Painel de Análise COVID-19")

# Carregar dados
df = carregar_dados()

# Lista de países
paises = sorted(df["location"].dropna().unique())

# Sidebar para seleção
st.sidebar.header("⚙️ Filtros")
pais = st.sidebar.selectbox("Selecione um país", paises)
datas = st.sidebar.date_input(
    "Selecione intervalo de datas",
    [df["date"].min(), df["date"].max()]
)

# Filtrar por país e datas
try:
    df_pais = df[df["location"] == pais]
    if isinstance(datas, list) and len(datas) == 2:
        inicio, fim = datas
        df_pais = df_pais[(df_pais["date"] >= pd.to_datetime(inicio)) &
                          (df_pais["date"] <= pd.to_datetime(fim))]
except Exception as e:
    st.error(f"Erro ao filtrar dados: {e}")

# Mostrar dados
st.subheader(f"📍 Dados para {pais}")
st.dataframe(df_pais)

# Gráficos
try:
    st.line_chart(df_pais.set_index("date")[["new_cases", "new_deaths"]])
    if "people_fully_vaccinated_per_hundred" in df_pais.columns:
        st.line_chart(df_pais.set_index("date")[["people_fully_vaccinated_per_hundred"]])
except Exception as e:
    st.warning(f"Não foi possível gerar gráficos: {e}")
