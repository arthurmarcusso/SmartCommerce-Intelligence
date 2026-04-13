import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from loguru import logger
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

sys.path.append(str(Path(__file__).resolve().parents[1] / "ETL"))
from db import get_engine

MODELS_DIR = Path(__file__).parent / "models"
MODELS_DIR.mkdir(exist_ok=True)


def treinar_regressao(engine):
    logger.info("Treinando regressão linear...")

    df = pd.read_sql(
        "SELECT data, receita_total FROM metricas_diarias ORDER BY data",
        engine
    )

    df["data"] = pd.to_datetime(df["data"])
    df["dia_numero"] = (df["data"] - df["data"].min()).dt.days

    X = df[["dia_numero"]]
    y = df["receita_total"]

    modelo = LinearRegression()
    modelo.fit(X,y)

    joblib.dump(modelo, MODELS_DIR / "regressao_receita.pkl")
    joblib.dump(df["data"].min(), MODELS_DIR / "regressao_data_inicio.pkl")
    logger.success("Regressão salva.")  

def treinar_anomalias(engine):
    logger.info("Treinando Isolation Forest...")

    df = pd.read_sql( 
        "SELECT receita_total, total_pedidos, ticket_medio FROM metricas_diarias", 
        engine
    )

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df)

    modelo = IsolationForest(contamination=0.05, random_state=42)
    modelo.fit(X_scaled)

    joblib.dump(modelo, MODELS_DIR / "isolation_forest.pkl")
    joblib.dump(scaler, MODELS_DIR / "scaler_anomalias.pkl")
    logger.success("Isolation Forest salvo.")

#modelo RFM: recência, frequência e valor monetário
def treinar_kmeans(engine):
    logger.info("Treinando K-Means RFM...")

    df = pd.read_sql("""
            select  c.id as cliente_id, DATEDIFF(CURDATE(), MAX(p.data_pedido)) as recencia,
                    COUNT(p.id) as frequencia,
                    SUM(p.valor_total) as valor_monetario
            from clientes c
            join pedidos p on p.cliente_id = c.id
            where p.status = 'concluido'
            group by c.id
         """, engine)
    
    df.dropna(inplace=True)

    scaler = StandardScaler()
    X_Scaled = scaler.fit_transform(df[["recencia", "frequencia", "valor_monetario"]])

    modelo = KMeans(n_clusters=4, random_state=42, n_init=10)
    modelo.fit(X_Scaled)

    #coluna contendo separação dentre 4 categorias de clientes (n_clusters=4)
    df["cluster"] = modelo.labels_

    joblib.dump(modelo, MODELS_DIR / "kmeans_rfm.pkl")
    joblib.dump(scaler, MODELS_DIR / "scaler_rfm.pkl")
    joblib.dump(df, MODELS_DIR / "rfm_com_clusters.pkl")
    logger.success("K-Means salvo.")


def main():
    engine = get_engine()
    treinar_regressao(engine)
    treinar_anomalias(engine)
    treinar_kmeans(engine)
    logger.info("Todos os modelos treinados e salvos!")


if __name__ == "__main__":
    main()