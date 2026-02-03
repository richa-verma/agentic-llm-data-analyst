import sqlite3

def query_sql(query: str):
    conn = sqlite3.connect("data/assets.db")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    conn.close()
    return str(rows)
