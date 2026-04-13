import sys
import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "ETL"))
from db import get_engine

MODELS_DIR = Path(__file__).resolve().parents[1] / "ML" / "models"

st.set_page_config(
    page_title= "SmartCommerce Intelligence",
    page_icon= "🛒",
    layout= "wide",
)

engine = get_engine()

#300 segundos para cada query no banco
@st.cache_data(ttl=300)
def load_metricas():
    return pd.read_sql(
        "SELECT * from metricas_diarias order by data",
        engine
    )

@st.cache_data(ttl=300)
def load_categorias():
    return pd.read_sql(
        """select p.category, count(ip.id) as total_itens, sum(ip.preco_unit * ip.quantidade) as receita_total
           from itens_pedido ip 
           join produtos p on ip.produto_id = p.id
           group by p.category 
           order by receita_total DESC        
        """, engine
    )

@st.cache_data(ttl=300)
def load_rfm():
    return joblib.load(MODELS_DIR / "rfm_com_clusters.pkl") 


#cabeçalho e KPIs
st.title("🛒 SmartCommerce Intelligence")
st.caption("Dashboard de análise de vendas com IA")

metricas   = load_metricas()
categorias = load_categorias()
rfm        = load_rfm()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita Total", f"R$ {metricas['receita_total'].sum():,.2f}")
col2.metric("Total de Pedidos", f"{metricas['total_pedidos'].sum():,}")
col3.metric("Ticket Médio", f"R$ {metricas['ticket_medio'].mean():,.2f}")
col4.metric("Dias Analisados", len(metricas))

st.divider()

#grafico de receita diária
st.subheader("Receita Diária")
fig = px.line(
    metricas,
    x="data",
    y="receita_total",
    labels = {"data": "Data", "receita_total": "Receita (R$)"},
    template = "plotly_white"
)

st.plotly_chart(fig, width="stretch")

st.divider()

#receita por categoria e previsão
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Receita por categoria")
    fig_bar = px.bar(
        categorias.sort_values("receita_total", ascending=True),
        x="receita_total",
        y="category",
        orientation="h",
        labels={"receita_total": "Receita (R$)", "category":"Categoria"},
        template="plotly_white",
    )
    st.plotly_chart(fig_bar, width="stretch")

with col_b:
    st.subheader("Previsão de receita — próximos 7 dias")
    try:
        modelo = joblib.load(MODELS_DIR / "regressao_receita.pkl")
        data_inicio = joblib.load(MODELS_DIR / "regressao_data_inicio.pkl")

        ultimo_dia = (pd.Timestamp(metricas["data"].max()) - pd.Timestamp(data_inicio)).days
        dias_futuros = np.array(range(ultimo_dia + 1, ultimo_dia + 8)).reshape(-1,1) 
        previsoes = modelo.predict(dias_futuros)

        datas_futuras = pd.date_range(
            start = pd.Timestamp(metricas["data"].max()) + pd.Timedelta(days=1), periods=7
        )
        df_prev = pd.DataFrame(
            {
                "data": datas_futuras,
                "receita_prevista": previsoes.round(2)
            }
        )
        fig_prev = px.bar(
            df_prev,
            x="data",
            y="receita_prevista",
            labels = {"data": "Data", "receita_prevista": "Receita Prevista (R$)"},
            template="plotly_white",
        )
        st.plotly_chart(fig_prev, width="stretch")
    except:
        st.info("Execute o Módulo 3 para ver as previsões.")

st.divider()

#segmentação de clientes
st.subheader("Segmentação de clientes - K-Means RFM")
st.caption("Cada ponto é um cliente. As cores representam os 4 grupos identificados pelo modelo.")

rfm["cluster"] = rfm["cluster"].astype(str)

fig_scatter = px.scatter(
    rfm,
    x = "frequencia",
    y = "valor_monetario",
    color = "cluster",
    hover_data=["cliente_id", "recencia"],
    labels={
        "frequencia": "Frequência de compras",
        "valor_monetario": "Valor total gasto (R$)",
        "cluster": "Segmento",
    },
    template="plotly_white",
)
st.plotly_chart(fig_scatter, width="stretch")
