# questpd

**questpd** is a lightweight Python client that simplifies interactions between [QuestDB](https://questdb.io) and `pandas`. It provides a convenient wrapper for ingesting, querying, and managing QuestDB tables with minimal boilerplate.

## 🚀 Features

- Query QuestDB and return results as `pandas.DataFrame`
- Ingest dataframes into QuestDB using the high-performance line protocol
- Create and truncate tables
- Check if a table exists
- Clean, simple Python API

---

## 📦 Installation

You can install `questpd` directly from a Bitbucket repository:

```bash
pip install git+https://bitbucket.org/<your_username>/questpd.git#egg=questpd
```

Or via SSH for private repos:

```bash
pip install git+ssh://git@bitbucket.org/<your_username>/questpd.git#egg=questpd
```

## 🛠 Usage

### Initialise the Client

```python
from questpd import qdbClient

client = qdbClient(
    host=HOST,        # QuestDB host
    front_port=9000,    # HTTP Line protocol port
    back_port=8812,     # PostgreSQL wire protocol port
    user=USERNAME,    # QuestDB username
    password=PASSWORD, # QuestDB password
    database="qdb" # QuestDB database name
)
```
### Query data from QuestDB

```python
df = client.query("SELECT * FROM my_table WHERE time > now - 1h")
print(df)
```
### Upload a DataFrame to QuestDB

```python
import pandas as pd

df = pd.DataFrame({
    "timestamp": pd.date_range("2023-01-01", periods=3, freq="T"),
    "symbol": ["AAPL", "GOOG", "MSFT"],
    "price": [150.0, 2700.0, 310.0]
})

client.upload_to_qdb(df, table_name="trades", ts="timestamp")
```
### Create a table

```python
column_definitions = {
    "timestamp": "TIMESTAMP",
    "symbol": "SYMBOL",
    "price": "DOUBLE"
}

client.create_table(
    table_name="trades",
    column_dict=column_definitions,
    ts_column="timestamp",
    partition="DAY",
    dedup="symbol"
)
```
### Truncate a table

```python
client.truncate_table("trades")

exists = client.check_table_exists("trades")
print(f"Table exists? {exists}")
```

## 🧾 Requirements

- `pandas`
- `requests`
- `psycopg2` (for PostgreSQL wire protocol)

Install dependencies via:

```bash
pip install -r requirements.txt
```

## 📂 Project Structure

```bash
questpd/
├── questpd/
│   ├── __init__.py
│   └── client.py
├── README.md
├── requirements.txt
├── setup.py
```