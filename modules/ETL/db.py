import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


def get_engine():
    host = os.getenv("DB_HOST","localhost")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "smartcomerce")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"
    engine = create_engine(url, echo=False)
    logger.info(f"Conexão Criada: {host}:{port}/{name}")
    return engine