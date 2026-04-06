import random
import pandas as pd
from faker import Faker
from pathlib import Path
from loguru import logger

fake = Faker('pt_BR')
random.seed(42)
Faker.seed(42)

OUTPUT_DIR = Path('__file__').resolve().parents[0] / "data" / "synthetic"

NUM_clientes = 500
NUM_pedidos = 2000
NUM_produtos = 100

#gerador de clientes

SEGMENTOS = ['premium', 'regular', 'inativo']

def gerar_clientes():
    logger.info(f"Gerando {NUM_clientes}")
    clientes = []
    for i in range (1, NUM_clientes+1):
        clientes.append(
            {"id": i,
             "nome":fake.name(),
             "email": fake.unique.email(),
             "cidade": fake.city(),
             "estado": fake.estado_sigla(),
             "segmento": random.choices(SEGMENTOS, weights=[0.2, 0.6, 0.2])[0],
             }
        )
    return pd.DataFrame(clientes)

#gerador de pedidos

STATUS = ["concluido", "cancelado", "devolvido"]

def gerar_pedidos():
    logger.info(f"Gerando {NUM_pedidos} pedidos...")
    pedidos = []
    for i in range(1, NUM_pedidos+1):
        pedidos.append(
            {
                "id":i,
                "cliente_id": random.randint(1, NUM_clientes),
                "data_pedido": fake.date_between(
                    start_date="-1y",
                    end_date = "today").strftime("%Y-%m-%d"),
                "status": random.choices(STATUS, weights=[0.85, 0.10, 0.05])[0],
                "valor_total" : round(random.uniform(50, 1500), 2),
             }
        )
    return pd.DataFrame(pedidos)

#gerador de itens do pedido

def gerar_itens(pedidos):
    logger.info("Gerando itens de pedido...")
    itens = []
    item_id = 1
    for _, pedido in pedidos.iterrows():
        num_itens = random.randint(1, 5)
        for _ in range(num_itens):
            quantidade = random.randint(1, 4)
            preco_unit = round(random.uniform(10, 500), 2)
            itens.append({
                "id":         item_id,
                "pedido_id":  pedido["id"],
                "produto_id": random.randint(1, NUM_produtos),
                "quantidade": quantidade,
                "preco_unit": preco_unit,
            })
            item_id += 1
    return pd.DataFrame(itens)

def salvar(df, nome):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    caminho = OUTPUT_DIR / nome
    df.to_csv(caminho, index=False, encoding="utf-8")
    logger.success(f"Salvo: {caminho}  ({len(df)} linhas)")


def main():
    clientes = gerar_clientes()
    pedidos  = gerar_pedidos()
    itens    = gerar_itens(pedidos)

    salvar(clientes, "clientes.csv")
    salvar(pedidos,  "pedidos.csv")
    salvar(itens,    "itens_pedido.csv")

    logger.info("Geração de dados sintéticos concluída.")


if __name__ == "__main__":
    main()