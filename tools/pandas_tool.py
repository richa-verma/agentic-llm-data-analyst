import sqlite3
import pandas as pd

def pandas_analysis():
    conn = sqlite3.connect("data/assets.db")
    df = pd.read_sql_query("SELECT * FROM asset_usage", conn)
    conn.close()

    summary = df.groupby("asset_id")["energy_kwh"].mean()
    return summary.to_string()
