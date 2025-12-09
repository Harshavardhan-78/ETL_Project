Below is a clean **README.md** you can use for your ETL Weather Pipeline.
It is fully aligned with your files:


# **Weather ETL Pipeline using Open-Meteo API & Supabase**

This project implements a complete **ETL (Extract–Transform–Load) pipeline** for weather data using the **Open-Meteo API**, processing hourly weather metrics for Hyderabad and inserting them into a **Supabase PostgreSQL database**.

---

# 📌 **Pipeline Overview**

```
Extract → Transform → Load → Supabase
```

### ✔ Extract

Fetch hourly weather data from **Open-Meteo API** and store it as raw JSON.

### ✔ Transform

Clean, standardize, and convert the JSON into a tabular CSV.

### ✔ Load

Insert final clean weather data into the **weather_data** table in Supabase.

---

# 📁 **Project Folder Structure**

```
ETL_Weather/
│
├── Scripts/
│   ├── Extractweather.py        # Extract step
│   ├── Tr_weather.py            # Transform step
│   └── Loadweather.py           # Load step
│
├── data/
│   ├── raw/                     # Raw JSON files (extracted)
│   └── staged/                  # Clean CSV (transformed)
│
└── README.md
```

---

# 🔍 **1. Extract Step**

### File: `Extractweather.py`

Extracts live weather data from Open-Meteo API.

Uses:

* temperature
* humidity
* wind speed
* timestamps

Each run saves a file like:

```
data/raw/weather_YYMMDD_HHMMSS.json
```

Sample raw file: 

---

# 🔄 **2. Transform Step**

### File: `Tr_weather.py`

Transforms the **latest** raw JSON file into a clean DataFrame.

Source fields → Target fields:

| Raw Key               | Final Column      |
| --------------------- | ----------------- |
| temperature_2m        | temperature_c     |
| relative_humidity_2m  | humidity_percent  |
| wind_speed_10m        | wind_speed_kmph   |
| time                  | time              |
| + city added manually | Hyderabad         |
| extracted_at          | current timestamp |

Saves output:

```
data/staged/weather_cleaned.csv
```

Implementation: 

---

# 📥 **3. Load Step**

### File: `Loadweather.py`

Loads the cleaned CSV into the Supabase table:

```
weather_data
```

Table columns:

```sql
id BIGSERIAL PRIMARY KEY,
time TIMESTAMP,
temperature_c DOUBLE PRECISION,
humidity_percent DOUBLE PRECISION,
city TEXT,
extracted_at TIMESTAMP,
wind_speed_kmph DOUBLE PRECISION
```

This step:

✔ Converts timestamps to string ISO format
✔ Renames CSV fields to match DB columns
✔ Inserts in batches of 20
✔ Sleeps to avoid Supabase rate limiting

Implementation: 

---

# 🗄 **Supabase Weather Table Schema**

```sql
CREATE TABLE weather_data(
    id BIGSERIAL PRIMARY KEY,
    time TIMESTAMP,
    temperature_c DOUBLE PRECISION,
    humidity_percent DOUBLE PRECISION,
    city TEXT,
    extracted_at TIMESTAMP
);

ALTER TABLE weather_data
ADD COLUMN wind_speed_kmph DOUBLE PRECISION;
```

---

# 🚀 **How to Run the ETL**

### Step 1 — Extract

```
python Scripts/Extractweather.py
```

### Step 2 — Transform

```
python Scripts/Tr_weather.py
```

### Step 3 — Load

```
python Scripts/Loadweather.py
```

All done! Your Supabase table will now contain up-to-date hourly weather data.

---

# ⚠ Requirements

Install dependencies:

```
pip install requests pandas supabase python-dotenv
```

---

# 🎯 **Future Enhancements**

* Automate ETL using cron / Windows Task Scheduler
* Store city dynamically
* Log processing steps
* Add error-handling and retry logic
* Support multiple cities

---


