import sys
import pandas as pd
from pathlib import Path
from loguru import logger

sys.path.append(str(Path(__file__).resolve().parent))
from db import get_engine

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"
SYNTHETIC_DIR = Path(__file__).resolve().parents[2] / "data" / "synthetic"

#extract
def extrair():
    logger.info("Extraindo dados dos CSVs...")
    return {
        "produtos": pd.read_csv(RAW_DIR / "produtos.csv"),
        "clientes": pd.read_csv(SYNTHETIC_DIR / "clientes.csv"),
        "pedidos": pd.read_csv(SYNTHETIC_DIR / "pedidos.csv", parse_dates=["data_pedido"]),
        "itens_pedido": pd.read_csv(SYNTHETIC_DIR / "itens_pedido.csv"),
    }

#transform
def transformar(dfs):
    logger.info("Transformando dados...")

    #produtos
    produtos = dfs["produtos"].copy()
    produtos["price"] = pd.to_numeric(produtos["price"], errors = "coerce")
    produtos["category"] = produtos["category"].str.strip().str.lower()
    produtos.dropna(subset = ["id", "price"], inplace = True)

    #clientes
    clientes = dfs["clientes"].copy()
    clientes["segmento"] = clientes["segmento"].str.lower()

    #pedidos
    pedidos = dfs["pedidos"].copy()
    pedidos = pedidos[pedidos["status"] == "concluido"].copy()
    pedidos["valor_total"] = pd.to_numeric(pedidos["valor_total"], errors = "coerce")
    pedidos.dropna(subset=["valor_total"], inplace = True)

    #itens
    itens = dfs["itens_pedido"].copy()
    itens["preco_unit"] = pd.to_numeric(itens["preco_unit"], errors="coerce")
    itens["quantidade"] = pd.to_numeric(itens["quantidade"], errors="coerce")
    itens.dropna(inplace=True)

    #verificação de itens existentes em pedidos
    ids_pedidos_validos = set(pedidos["id"])
    itens = itens[itens["pedido_id"].isin(ids_pedidos_validos)].copy()

    metricas = (
        pedidos.groupby("data_pedido")
        .agg(
            total_pedidos = ("id", "count"),
            receita_total = ("valor_total", "sum"),
        )
        .reset_index()
    )
    metricas.rename(columns={"data_pedido": "data"}, inplace = True)

    logger.success("Transformação concluída!")
    return {
        "produtos": produtos,
        "clientes": clientes,
        "pedidos": pedidos,
        "itens_pedido": itens,
        "metricas_diarias": metricas,
    }

#load
def carregar(dfs, engine):
    logger.info("Carregando dados no MySQL...")

    tabelas = [
        ("itens_pedido", "itens_pedido"),
        ("metricas_diarias", "metricas_diarias"),
        ("pedidos", "pedidos"),
        ("clientes", "clientes"),
        ("produtos", "produtos"),
    ]

    for chave, tabela in tabelas:
        df = dfs[chave]
        df.to_sql(
            name = tabela,
            con = engine,
            if_exists = "replace",
            index = False,
            chunksize=500,
        )
        logger.success(f"tabela '{tabela}' carregada - {len(df)} linhas.")
    

def main():
    engine = get_engine()
    dados_brutos = extrair()
    dados_processados = transformar(dados_brutos)
    carregar(dados_processados, engine)
    logger.info('Pipeline ETL finalizado com sucesso!')

if __name__ == "__main__":
    main()