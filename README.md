# 🛒 SmartCommerce Intelligence Platform

Pipeline completo de inteligência de dados para e-commerce — da ingestão de dados brutos até um dashboard interativo com modelos de machine learning e banco de dados em nuvem.

> Projeto desenvolvido para praticar engenharia de dados na prática, cobrindo todas as etapas de um pipeline real.

🔗 **[Acesse o dashboard ao vivo](https://smartcommerce-intelligence.streamlit.app/)**

---

## O que esse projeto faz

- Coleta produtos reais de uma API externa (DummyJSON)
- Gera dados sintéticos realistas de clientes e pedidos com Faker
- Processa e carrega tudo num banco MySQL em nuvem (Clever Cloud) via pipeline ETL
- Treina três modelos de machine learning sobre os dados
- Exibe tudo num dashboard interativo publicado no Streamlit Cloud

---

## Arquitetura
```
API Externa + Faker
        │
        ▼
[ ETL — Python + Pandas ]
        │
        ▼
 [ MySQL — Clever Cloud ]
        │
   ┌────┴────┐
   ▼         ▼
 [ ML ]  [ Dashboard ]
scikit    Streamlit
-learn
```

---

## Tecnologias utilizadas

| Ferramenta | Uso |
|------------|-----|
| Python 3.11 | Linguagem principal |
| Pandas | Limpeza e transformação de dados |
| MySQL + SQLAlchemy | Armazenamento e consulta |
| Clever Cloud | Hospedagem do banco em nuvem |
| scikit-learn | Modelos de ML |
| Streamlit | Dashboard interativo |
| Plotly | Gráficos interativos |
| Faker | Geração de dados sintéticos |
| n8n | Automação de alertas (em desenvolvimento) |

---

## Modelos de Machine Learning

**Regressão Linear** — prevê a receita dos próximos 7 dias com base no histórico de vendas.

**Isolation Forest** — detecta dias com comportamento anômalo de vendas, como quedas ou picos fora do padrão.

**K-Means (RFM)** — segmenta clientes em 4 grupos com base em recência, frequência e valor gasto.

---

## Como rodar localmente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/smartcommerce-intelligence.git
cd smartcommerce-intelligence

# Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as credenciais
cp .env.example .env
# edite o .env com suas credenciais MySQL

# Execute o pipeline na ordem
python modules/ingestion/fetch_api.py
python modules/ingestion/generate_synthetic.py
python modules/ETL/run_pipeline.py
python modules/ML/train_models.py

# Inicie o dashboard
streamlit run modules/dashboard/app.py
```

---

## Estrutura do projeto

```
smartcommerce-intelligence/
│
├── data/
│   ├── raw/              # Dados brutos da API
│   └── synthetic/        # Dados gerados com Faker
│
├── modules/
│   ├── ingestion/        # Coleta de dados
│   ├── ETL/              # Pipeline de transformação e carga
│   ├── ML/               # Modelos de machine learning
│   └── dashboard/        # Aplicação Streamlit
│
├── sql/                  # Scripts de criação do banco
├── .env.example          # Modelo de configuração
├── runtime.txt           # versão do python utilizada
└── requirements.txt      # Dependências
```

---

## Autor

Desenvolvido por Arthur Marcusso — estudante de IA & Ciência de Dados.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://linkedin.com/in/arthurmarcusso)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/arthurmarcusso)
