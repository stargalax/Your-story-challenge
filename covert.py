import pandas as pd
import sqlite3

df = pd.read_excel("statewise.xlsx")

conn = sqlite3.connect("heritage.db")
df.to_sql("HERITAGE_DATA", conn, if_exists="replace", index=False)
conn.close()
