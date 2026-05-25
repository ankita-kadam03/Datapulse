# DataPulse 🚀
### Production-Ready Retail ETL & Analytics Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
![Airflow](https://img.shields.io/badge/Airflow-2.8.1-green)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

---

## What is DataPulse?

DataPulse is a production-ready **end-to-end retail data pipeline** that:

- **Extracts** raw sales data from CSV sources (9,994 records)
- **Transforms** and validates the data (removes duplicates, nulls, invalid records)
- **Loads** clean data into a PostgreSQL data warehouse (star schema)
- **Automates** the entire pipeline using Apache Airflow (runs daily)
- **Visualizes** business KPIs using Power BI dashboards

> Built to simulate a real-world retail analytics system like Amazon, Flipkart, or DMart.

---

## Architecture

```
Raw CSV Data (Superstore)
        ↓
   [ Extract ]
   Python Script
        ↓
   [ Transform ]
   Pandas - Clean & Validate
        ↓
   [ Load ]
   PostgreSQL - Star Schema
        ↓
   [ Automate ]
   Apache Airflow DAG
        ↓
   [ Visualize ]
   Power BI Dashboard
```

---

## Star Schema

```
customer_dim ──┐
product_dim  ──┤──► sales_fact (9,986 rows)
store_dim    ──┤
date_dim     ──┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| ETL | Python 3.8, Pandas |
| Database | PostgreSQL 15 |
| Scheduling | Apache Airflow 2.8.1 |
| Containerization | Docker + Docker Compose |
| Dashboard | Power BI Desktop |
| Version Control | Git + GitHub |

---

## Project Structure

```
datapulse/
├── dags/
│   └── datapulse_dag.py       # Airflow DAG - 4 task pipeline
├── extraction/
│   └── extract.py             # Read & split raw CSV data
├── transformation/
│   └── transform.py           # Clean, validate, build dimensions
├── loading/
│   └── load.py                # Load into PostgreSQL star schema
├── sql/
│   └── init.sql               # Star schema DDL + views
├── tests/
│   └── test_transform.py      # Data quality tests
├── logs/                      # ETL run logs
├── dashboards/                # Power BI dashboard files
├── docker-compose.yml         # PostgreSQL + Airflow setup
├── requirements.txt
└── README.md
```

---

## Quick Start

### Prerequisites
- Docker Desktop
- Python 3.8+
- Power BI Desktop (free)

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/datapulse-retail-analytics.git
cd datapulse-retail-analytics
```

### 2. Setup environment
```bash
cp .env.example .env
# Generate Fernet key and add to .env
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 3. Download dataset
Download [Superstore Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) and place it at `data/superstore.csv`

### 4. Start Docker containers
```bash
docker-compose up -d
```

### 5. Run ETL pipeline manually
```bash
python extraction/extract.py
python loading/load.py
```

### 6. Open Airflow UI
```
http://localhost:8080
Username: admin
Password: admin
```
Trigger the `datapulse_superstore_etl` DAG

---

## Pipeline Results

| Table | Records |
|---|---|
| customer_dim | 793 unique customers |
| product_dim | 1,862 unique products |
| date_dim | 1,237 unique dates |
| sales_fact | 9,986 clean records |
| Total Sales | $2.3 Million |
| Total Profit | $286,397 |

---

## Dashboard KPIs

- 📈 Total Revenue & Profit
- 📅 Monthly Sales Trend
- 🏆 Top 10 Products by Sales
- 🗺️ Region-wise Performance
- 👥 Customer Segment Analysis
- 📦 Category & Sub-category Breakdown

---

## Resume Line

> Built **DataPulse**, a production-ready retail ETL and analytics platform using Python, PostgreSQL, Apache Airflow, and Docker. Automated daily data pipelines processing 9,994 records with star schema modeling and Power BI dashboards showing $2.3M in retail sales insights.

---

## Author

**Your Name**  
[LinkedIn](#) | [GitHub](#)