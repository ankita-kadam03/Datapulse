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
git clone https://github.com/ankita-kadam03/Datapulse.git
cd Datapulse
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

## Power BI Dashboard

The dashboard is built manually in **Power BI Desktop** by connecting directly to the PostgreSQL warehouse.

### Step 1 — Connect Power BI to PostgreSQL

1. Open **Power BI Desktop** (free download from [here](https://powerbi.microsoft.com/desktop))
2. Click **Get Data** → search **PostgreSQL** → click **Connect**
3. Enter connection details:
   - Server: `localhost`
   - Database: `datapulse_db`
4. Enter credentials:
   - Username: `datapulse`
   - Password: `datapulse123`
5. Select these tables and click **Load**:
   - `sales_fact`
   - `customer_dim`
   - `product_dim`
   - `date_dim`
   - `v_sales_summary`

### Step 2 — Create DAX Measures

In the **sales_fact** table, create these measures one by one  
(**Home → New Measure**):

```dax
Total Sales = SUM(sales_fact[total_amount])

Total Profit = SUM(sales_fact[profit])

Total Orders = DISTINCTCOUNT(sales_fact[order_id])

Total Customers = DISTINCTCOUNT(sales_fact[customer_id])

Profit Margin % = DIVIDE([Total Profit], [Total Sales]) * 100

Avg Order Value = DIVIDE([Total Sales], [Total Orders])
```

### Step 3 — Build the Visuals

| Visual | Type | Fields |
|---|---|---|
| Total Sales | Card | `[Total Sales]` |
| Total Profit | Card | `[Total Profit]` |
| Total Orders | Card | `[Total Orders]` |
| Total Customers | Card | `[Total Customers]` |
| Monthly Revenue Trend | Line Chart | Axis: `date_dim[month_name]` · Values: `[Total Sales]`, `[Total Profit]` |
| Sales by Region | Bar Chart | Axis: `sales_fact[region]` · Values: `[Total Sales]` |
| Sales by Category | Donut Chart | Legend: `product_dim[category]` · Values: `[Total Sales]` |
| Top Products | Table | `product_dim[sub_category]`, `[Total Sales]`, `[Total Profit]` |

### Step 4 — Add Slicers (Filters)

Add 4 slicers on the right side of the canvas:

- `date_dim[year]` → filter by Year
- `sales_fact[region]` → filter by Region
- `product_dim[category]` → filter by Category
- `customer_dim[segment]` → filter by Segment

### Step 5 — Save

Save the file as `dashboards/DataPulse.pbix` inside the project folder.

---

## Dashboard KPIs

- 💰 Total Revenue & Profit cards
- 📈 Monthly Sales Trend (line chart)
- 📊 Sales by Region (bar chart)
- 🍩 Sales by Category (donut chart)
- 🏆 Top Products by Sub-Category (table)
- 🔽 Slicers: Year / Region / Category / Segment

---

## Author

**Ankita Kadam**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-ankita--kadam03-blue?logo=linkedin)](https://www.linkedin.com/in/ankita-kadam03/)
[![GitHub](https://img.shields.io/badge/GitHub-ankita--kadam03-black?logo=github)](https://github.com/ankita-kadam03)