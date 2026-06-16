# ⚽ Copa 2026 - Data Engineering Pipeline

A real-time data pipeline for the 2026 FIFA World Cup, built with modern data engineering tools.

## 🏗️ Architecture

- **Ingestion:** Python + REST API (football-data.org)
- **Orchestration:** Apache Airflow
- **Storage:** PostgreSQL + Data Lake (raw / trusted / refined)
- **Transformation:** Pandas + dbt
- **Dashboard:** Streamlit

## 🛠️ Tech Stack

- Python 3.12
- Apache Airflow 2.9.1
- PostgreSQL 15
- Docker + Docker Compose
- dbt (coming soon)

## 🚀 How to run

1. Clone the repository
2. Create a `.env` file with your API key:
API_KEY=your_api_key_here
3. Start the containers:
```bash
   docker compose up -d
```
4. Access Airflow at `http://localhost:8080`
5. Trigger the `dag_get_games` DAG

## 📊 Data Flow

raw → trusted → refined

Data is collected hourly from the football-data.org API and stored in layers.

## 📝 License
MIT