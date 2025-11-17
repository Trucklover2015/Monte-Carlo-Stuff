import requests
import pandas as pd

url =

response = request.get(url)


tables = pd.read_html(response.text)

print(f"Found {len(tables)} tables on the page.")

ppg_table = tables[0]
print(ppg_table.head())
print(ppg_table.columns)
