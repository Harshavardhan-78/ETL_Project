# 🚀 NASA APOD ETL Pipeline – Project Description

This project implements a complete **ETL (Extract–Transform–Load)** pipeline that collects NASA's **Astronomy Picture of the Day (APOD)** data, processes it into a structured format, and loads it into a **Supabase PostgreSQL database** for analytics or dashboarding.

The pipeline is designed to be modular, production-friendly, and easy to automate (cron, Airflow, GitHub Actions, etc.).

---

## 🔍 **📌 1. Extract – Fetch Daily NASA APOD Data**

The **Extract.py** script connects to the NASA APOD API using an API key stored in `.env`.

It performs the following:

* Sends a request to NASA APOD endpoint
* Saves the JSON response into
  **`Data/raw/`** as a timestamped file
  Example:

  ```
  apod_251209_135202.json
  ```
* Downloads the APOD image (if available)
* Ensures reproducibility by storing raw responses without modification

This step guarantees that all raw API responses are archived for auditing or reprocessing.

---

## 🔧 **📌 2. Transform – Clean and Structure the Data**

The **Transform.py** script reads the latest raw JSON file and converts it into a clean, tabular format suitable for database insertion.

Key transformations include:

* Normalizing JSON keys to a consistent schema
* Cleaning and validating dates
* Generating a uniform `inserted_at` timestamp
* Handling missing fields gracefully
* Producing a CSV file stored in:
  **`Data/Staged/nasa_apod_staged.csv`**

This ensures the data is standardized and ready for loading.

---

## 🛢️ **📌 3. Load – Insert Into Supabase Database**

The **Load.py** script loads the transformed CSV into a Supabase PostgreSQL table named `nasa_apod`.

Operations performed:

* Reads the staged CSV file
* Converts NaN → NULL for database compatibility
* Formats dates and timestamps
* Inserts records in batches to avoid rate limits
* Logs progress and errors for transparency

The final table structure is:

```sql
CREATE TABLE nasa_apod (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    title VARCHAR(255) NOT NULL,
    explanation TEXT NOT NULL,
    media_type VARCHAR(50),
    image_url TEXT,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

This enables running analytics, dashboards, or machine learning using APOD metadata.

---

## 📁 **Project Structure**

```
ETL_NASA/
│
├── Data/
│   ├── raw/          ← Raw JSON API responses
│   ├── Staged/       ← Cleaned CSV output
│
├── Scripts/
│   ├── Extract.py    ← Fetches NASA APOD + images
│   ├── Transform.py  ← Converts JSON → structured CSV
│   ├── Load.py       ← Loads data into Supabase
│
├── .env              ← API keys (NASA + Supabase)
└── README.md
```

---

## 🧪 **Run the Pipeline**

```bash
python Scripts/Extract.py
python Scripts/Transform.py
python Scripts/Load.py
```

---

## 🎯 Summary

This ETL pipeline provides:

* Automated ingestion of NASA APOD data
* Normalized and clean datasets
* Database-ready output for analytics
* Reproducible and maintainable architecture

Perfect for learning ETL concepts, building dashboards, or powering a data portfolio project.

---
