import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from loguru import logger
import sys
from pathlib import Path
load_dotenv()

def get_engine():
    #tentando pegar as credenciais do Streamlit secrets, se não funcionar, pega do .env
    try:
        import streamlit as st
        creds = st.secrets["mysql"]
        host     = creds["host"]
        port     = creds["port"]
        name     = creds["database"]
        user     = creds["user"]
        password = creds["password"]
        logger.info("Usando credenciais do Streamlit secrets.")

    except Exception:
        host     = os.getenv("DB_HOST", "localhost")
        port     = os.getenv("DB_PORT", "3306")
        name     = os.getenv("DB_NAME", "smartcommerce")
        user     = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "")
        logger.info(f"Usando credenciais do .env: {host}:{port}/{name}")


    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"
    engine = create_engine(url, echo=False)
    logger.info(f"Conexão Criada: {host}:{port}/{name}")
    return engine