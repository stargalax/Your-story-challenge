import pandas as pd
import sqlite3

# Load Excel file
df = pd.read_excel("statewise.xlsx")

# Clean column names: strip, uppercase, replace spaces with _
df.columns = df.columns.str.strip().str.upper().str.replace(" ", "_")

# Drop junk columns (like 'UNNAMED: 8', etc.)
df = df.loc[:, ~df.columns.str.contains('^UNNAMED')]

# Optional: keep only needed columns
keep_cols = ['STATE', 'CITY_NAME', 'HERITAGE_NAME', 'HERITAGE_TYPE', 'LAT', 'LON']
df = df[keep_cols]

# Save to SQLite
conn = sqlite3.connect("heritage.db")
df.to_sql("HERITAGE_DATA", conn, if_exists="replace", index=False)
conn.close()

print("✅ Cleaned & saved to heritage.db")
