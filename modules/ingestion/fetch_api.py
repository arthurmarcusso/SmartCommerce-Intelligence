import requests
import pandas as pd
from pathlib import Path
from loguru import logger

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

API_URL = "https://dummyjson.com"

def fetch_produtos():
    logger.info("Iniciando a busca por produtos na API...")
    response = requests.get(f"{API_URL}/products?limit=100", timeout = 10)
    response.raise_for_status()
    produtos = response.json()["products"]
    logger.success(f"Produtos obtidos com sucesso! Total: {len(produtos)}")
    return produtos

COLUNAS_UTEIS = [
    "id","title","category","price","discountPercentage","rating",
    "stock","brand","availabilityStatus","minimumOrderQuantity"
]

def filtrar_colunas(produtos):
    df = pd.DataFrame(produtos)
    df = df[COLUNAS_UTEIS]
    logger.info(f'As colunas mantidas são: {df.columns.to_list()}')
    return df

def salvar_csv(df, nome_arquivo):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    caminho = OUTPUT_DIR / nome_arquivo
    df = pd.DataFrame(df)
    df.to_csv(caminho, index=False, encoding='utf-8')
    logger.success(f"Dados salvos em {caminho}")

def main():
    produtos = fetch_produtos()
    df = filtrar_colunas(produtos)
    salvar_csv(df, "produtos.csv")
    logger.info("Ingestão concluída com sucesso!")

if __name__ == "__main__":
    main()


